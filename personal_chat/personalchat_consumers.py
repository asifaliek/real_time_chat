from django.contrib.sites.shortcuts import get_current_site
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json
from .models import PersonalMessage, Thread
from django.contrib.auth.models import User
import base64
from chat.models import Room

class PersonalChatConsumer(WebsocketConsumer):
	def new_message(self, data):
		author = User.objects.get(username=data['author'])
		lobby = Thread.objects.get(id=data['lobby'])
		message = PersonalMessage.objects.create(
			sender=author,
			text=data['message'],
			thread=lobby)
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
			'author': message.sender.username,
			'content': message.text
		}

	commands = {
		'new_message': new_message,
	}

	def connect(self):
		protocol_path = self.scope['headers'][6][1]
		self.protocol_path = protocol_path.decode('utf-8')
		me = self.scope['user']
		other_person = self.scope['url_route']['kwargs']['username']
		other_user = User.objects.get(username=other_person)
		self.room_name = f'pearsonal_thread_{other_user.id}'
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
