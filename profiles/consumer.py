import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

        user = self.scope['user']
        profile_picture = await self.get_profile_picture(user=user)
        username = user.username

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'user_presence',
                'eventName':'joined',
                'username':username,
                'profile_picture':profile_picture
            }
        )
     

    async def receive(self, text_data):
        # Parse the incoming WebSocket message
        text_data_json = json.loads(text_data)
        message = text_data_json.get('message')

        # Get user info
        user = self.scope['user']
        profile_picture = await self.get_profile_picture(user=user)
        username = user.username

        # Broadcast the message to the group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username,
                'profile_picture': profile_picture,
            }
        )

    async def chat_message(self, event):
        # Send the broadcasted message to the WebSocket
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'username': event['username'],
            'profile_picture': event['profile_picture'],
        }))    


    async def user_presence(self, event):
        """
        Called when a message is sent to the group.
        """
        eventName = event.get('eventName', '')
        username = event.get('username', '')
        profile_picture = event.get('profile_picture')

        # Send the message to the WebSocket
        await self.send(text_data=json.dumps({
            'eventName': eventName,
            'username': username,
            'profile_picture': profile_picture,
        }))

    @database_sync_to_async
    def get_profile_picture(self, user):
        if user.is_authenticated and hasattr(user, 'profile'):
            return user.profile.image.url if user.profile.image else None
        return None      