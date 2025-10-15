# import libraries and modules
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import ChatMessage
from asgiref.sync import sync_to_async

# define ChatConsumer class
class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f"chat_{self.room_name}"
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
        history = await self.get_chat_history(self.room_name)
        for message in history:
            await self.send(text_data=json.dumps({
                'sender': message['sender'],
                'message': message['message']
            }))

    @sync_to_async
    def get_chat_history(self, room_name):
        return list(ChatMessage.objects.filter(room_name=room_name).values('sender', 'message').order_by('timestamp')[:50])  # Limit to 50 messages

    async def disconnect(self, close_code):
        # Leave the room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json.get('message')
        sender = text_data_json.get('sender', 'Anonymous')
        await self.save_message(self.room_name, sender, message)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': sender,
            }
        )

    async def chat_message(self, event):
        message = event['message']
        sender = event['sender']
        await self.send(text_data=json.dumps({
            'type': 'chat_message',
            'sender': sender,
            'message': message
        }))

    @sync_to_async
    def save_message(self, room_name, sender, message):
        ChatMessage.objects.create(room_name=room_name, sender=sender, message=message)
