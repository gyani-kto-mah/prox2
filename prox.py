from mitmproxy.http import HTTPFlow, HTTPResponse
import mitmproxy.net.http as HTTPHeaders
from websocket import create_connection as websocket_create_connection
from base64 import b64encode

ws = websocket_create_connection("ws://127.0.0.1:8000/ws")

class MakeHTTPRaw:
    def __init__(self, flow: HTTPFlow):
        if 'headers' not in dir(flow):
            raise TypeError('Invalid HTTP Request/Response passed.')
        self.flow = flow
        self.headers, self.body = self._parse()

    def _parse(self) -> (str, bytes):
        _headers, body = self.flow.headers, self.flow.raw_content
        headers = ''
        for _ in _headers:
            headers += f"{_}: {_headers[_]}\n"
        body = b'\n' + body
        return headers, body

    def raw_request(self) -> bytes:
        flow = self.flow
        raw_request = f"{flow.method} {flow.path} {flow.http_version}\n{self.headers}".encode()
        raw_request += self.body
        return raw_request

    def raw_response(self) -> bytes:
        flow = self.flow
        raw_response = f"{flow.http_version} {flow.status_code} {flow.reason}\n{self.headers}".encode()
        raw_response += self.body
        return raw_response


def request(flow: HTTPFlow):
    raw_req = MakeHTTPRaw(flow.request).raw_request()
    wsc = f'r:{b64encode(raw_req).decode()}'
    ws.send(wsc)


def response(flow: HTTPFlow):
    raw_resp = MakeHTTPRaw(flow.response).raw_response()
    wsc = f'R:{b64encode(raw_resp).decode()}'
    ws.send(wsc)


def error(flow: HTTPFlow):
    # TODO: signal of the error (verbose)
    wsc = f'e:{b64encode(ERROR).decode()}'
    ws.send(wsc)
