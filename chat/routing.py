from channels.routing import route

from . import consumers

channel_routing = [
	route('chat-messages', consumers.chat_messages),
	route('websocket.receive', consumers.ws_receive),
	route('websocket.connect', consumers.ws_connect),	
	route('websocket.disconnect', consumers.ws_disconnect),
]