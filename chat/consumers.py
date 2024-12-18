import json
from channels.generic.websocket import AsyncWebsocketConsumer
from django.utils.timezone import now

"""
This module defines the websocket consumer for the chat.

It handles websocket connections for real-time communication, connecting and disconnecting
from the chat room, receiving and sending messages.
"""

class ChatConsumer(AsyncWebsocketConsumer):
    """
    Websocket consumer for real-time chat.

    This consumer handles the websocket lifecycle of the chat room.
    """
    async def connect(self):
        """
        Handles the websocket connection request.

        This method is retrieves chat ID from the URL route and joins the chat room.
        Allowing this websocket consumer to receive messages from chat room.
        """
        self.chat_id = self.scope['url_route']['kwargs']['chat_id']
        self.chat_group_name = f'chat_{self.chat_id}'

        # Join room group
        await self.channel_layer.group_add(
            self.chat_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self):
        """
        Handles the websocket disconnection request.

        This method is removes the websocket connection from the chat room.
        """
        # Leave room group
        await self.channel_layer.group_discard(
            self.chat_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        """
        Recieves messages from chat room.

        Args:
            text_data (str): the incoming message as a JSON string.

        This method processes the recieved messages and sends it
        to the chat room.
        """
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        sender_username = self.scope['user'].username

        # Send message to room group
        await self.channel_layer.group_send(
            self.chat_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': sender_username,
                'timestamp': now().strftime('%H:%M'),
            }
        )

    async def chat_message(self, event):
        """
        Handles incoming messages from chat room.

        Args:
            event (dict): The event dict containing the message data.
                - message (str): The message content
                - sender (str): The sender username
                - timestamp (str): The timestamp of the message

        This method receives messages from chat room and send it to the websocket
        to be delivered to the connected client.
        """
        message = event['message']
        sender = event['sender']
        timestamp = event['timestamp']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender,
            'timestamp': timestamp
        }))
