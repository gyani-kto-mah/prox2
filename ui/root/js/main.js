const ws_url = "ws://127.0.0.1:8000/ws";
const ws_id = String(Math.random()).slice(2) + String(Date.now());  // This does leave a forensic trace, regarding when the js was probably loaded is an intended behavior.
const ws = new WebSocket(`${ws_url}/${ws_id}`);
const $ = document.querySelectorAll;


function send( input ) {
	if ( typeof(input) === 'object' ) {
		input = JSON.stringify(input);
	}
	ws.send(input);
}


ws.onmessage = function(event) {
	try {
		const data = event.data.split(':');
		const type = data[0];
		var ws_content = atob(data[1]);

		if ( type === 'r' ) {
			requestHandler(ws_content);
		
		} else if ( type === 'R' ) {
			responseHandler(ws_content);

		} else if ( type === 'e' ) {
			errorHandler(ws_content);

		} else if ( type === 'u' ) {
			// Unknown type, server side.
			unknownHandler(ws_content);

		} else {
			// Invalid type, logically.
			invalidHandler(event.data);

		}
	} catch ( DOMException ) {
		invalidHandler(event.data);
	}
}


function requestHandler( ws_content ) { console.info(ws_content); };
responseHandler = requestHandler;
errorHandler = responseHandler;


function unknownHandler( ws_content ) {
	console.warn(`Unknown websocket response:\n${ws_content}`);
}


function invalidHandler( data ) {
	console.error(`Weird webSocket response:\n${data}`)
}
