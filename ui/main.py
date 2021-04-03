#!/usr/bin/ev python3

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from typing import List
from base64 import b64decode, b64encode
from os.path import isfile
from fastapi.responses import FileResponse
from binascii import Error as IncorrectPaddingError


app = FastAPI()


def encode(ws_type, content):
    if type(content) != bytes:
        content = str(content).encode()
    content = b64encode(content).decode()
    msg = f'{ws_type}:{content}'
    return msg


def decode(data):
    if len(data.split(':')) == 2:
        ws_type, content = data.split(':')
        try:
            return ws_type, b64decode(content)
        except IncorrectPaddingError:
            return None, None
    return None, None


class WSConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, ws: WebSocket):
        await ws.accept()
        self.active_connections.append(ws)

    def disconnect(self, ws: WebSocket):
        self.active_connections.remove(ws)

    async def send_private_message(self, message: str, ws: WebSocket):
        await ws.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


wsm = WSConnectionManager()


@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    while True:
        data = await ws.receive_text()
        print(data)
        if data[0] == 'e':
            pass  # Do some random chikboom here.
        await wsm.broadcast(data)


@app.websocket("/ws/{client_id}")
async def websocket_endpoint(ws: WebSocket, client_id: int):
    await wsm.connect(ws)
    try:
        while True:
            data = await ws.receive_text()
            ws_type, content = decode(data)

            if not ws_type or not content:
                await ws.send_text(encode('e', 'Invalid input supplied.'))

            if ws_type == 'r':
                # TODO: Validate if raw HTTP here (content).
                # Request the given raw HTTP request.
                resp = f"FAKE RESP of {content}"
                await ws.send_text(encode('R', resp))
                return

            await ws.send_text(encode('u', data))
            # await wsm.send_private_message(f"You sent: {data}", ws)
            # await wsm.broadcast(f"Client #{client_id} sent: {data}")
    except WebSocketDisconnect:
        wsm.disconnect(ws)
        # await wsm.broadcast(f"Client #{client_id} left.")


@app.get('/')
def root():
	return FileResponse('root/index.html')


@app.get('/{filename:path}')
def files(filename):
    filepath = f'root/{filename}'
    supported_extensions = ('png', 'txt', 'js', 'ico', 'html', 'css', 'webmanifest')
    if filename.split('.')[-1] in supported_extensions and isfile(filepath):
        return FileResponse(filepath)
    raise HTTPException(
            status_code=404,
            detail=f"Requested file('/{filename}') does not exist."
        )
