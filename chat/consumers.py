import json
import re
import logging
from channels import Group, Channel
from channels.sessions import channel_session
from .models import Room

log = logging.getLogger(__name__)
pattern = re.compile(r'(?P<room>[a-z0-9\-]{1,50})/?$')


# Connected to websocket.connect
@channel_session
def ws_connect(message):
	match = pattern.search(message.content['path'])
	if match is None:
		log.debug('invalid path')
		return
	label = match.group('room')
	try:
		room = Room.objects.get(label=label)
	except Room.DoesNotExist:
		log.error('room does not exist, label={}'.format(label))
		return

	log.debug('connected to room={} client={}'.format(room.label, message.content['client']))

	Group('chat-{}'.format(room.label)).add(message.reply_channel)

	message.channel_session['room'] = room.label

	# Accept the connection request
	message.reply_channel.send({'accept': True})

# Connected to websocket.receive
@channel_session
def ws_receive(message):
	log.debug('received message: {}'.format(message.content['text']))
	# Stick the message onto the processing queue
	Channel('chat-messages').send({
		"room": message.channel_session['room'],
		"text": message.content['text'],
	})

# Connected to chat-messages
def chat_messages(message):
	log.debug('chat_messages')
	# Save to model
	label = message.content['room']
	try:
		room = Room.objects.get(label=label)
	except Room.DoesNotExist:
		log.error('received message, but room does not exist, label={}'.format(label))
		return

	try:
		data = json.loads(message.content['text'])
	except ValueError:
		log.debug('ws message isn\'t json text')
		return

	if set(data.keys()) != set(('handle', 'message')):
		log.debug('ws message - unexpected fomat')
		return

	log.debug('chat message room=%s handle=%s message=%s', 
			room.label, data['handle'], data['message'])

	msg = room.messages.create(**data)

	# Broadcast to listening sockets
	Group("chat-{}".format(room)).send({
		"text": json.dumps(msg.as_dict()),
	})

# Connected to websocket.disconnect
@channel_session
def ws_disconnect(message):
	try:
		Group("chat-{}".format(message.channel_session['room'])).discard(message.reply_channel)
	except KeyError as e:
		log.error(e)



