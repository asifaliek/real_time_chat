from django.contrib.sites.shortcuts import get_current_site
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json
from .models import Message, Room
from django.contrib.auth.models import User
import base64

class ChatConsumer(WebsocketConsumer):

	def new_message(self, data):
		author = User.objects.get(username=data['author'])
		room = Room.objects.get(id=data['room'])
		message = Message.objects.create(
			author=author,
			content=data['message'],
			room=room)
		content = {
			'command': 'new_message',
			'message': self.message_to_json(message)
		}
		return self.send_chat_message(content)

	def message_to_json(self, message):
		try:
			attachment = self.protocol_path+message.attachment.url
		except:
			attachment = None
		return {
			'id': message.id,
			'author': message.author.username,
			'content': message.content,
			'timestamp': str(message.timestamp),
			"attachment": attachment,
			"room_code": self.room_name
		}

	commands = {
		'new_message': new_message,
	}

	def connect(self):
		protocol_path = self.scope['headers'][6][1]
		self.protocol_path = protocol_path.decode('utf-8')
		self.room_name = self.scope['url_route']['kwargs']['room_code']
		self.user = self.scope["user"]
		self.room_group_name = 'chat_%s' % self.room_name
		async_to_sync(self.channel_layer.group_add)(
			self.room_group_name,
			self.channel_name
		)
		self.accept()

	def disconnect(self, close_code):
		async_to_sync(self.channel_layer.group_discard)(
			self.room_group_name,
			self.channel_name
		)

	def receive(self, text_data):
		data = json.loads(text_data)
		self.commands[data['command']](self, data)

	def send_chat_message(self, message):
		async_to_sync(self.channel_layer.group_send)(
			self.room_group_name,
			{
				'type': 'chat_message',
				'message': message
			}
		)

	def send_message(self, message):
		self.send(text_data=json.dumps(message))

	def chat_message(self, event):
		message = event['message']
		self.send(text_data=json.dumps(message))

