from channels import include, route

channel_routing = [
	include('chat.routing.channel_routing', path=r'^(?:/msg)?/chat'),
	route('chat-messages', 'chat.consumers.chat_messages'),
]