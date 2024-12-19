"""
This module defines the websocket URL routing for the chat app.

The routing links websocket endpoints to their respective consumers, enabling real-time
communication between websocket clients.
"""

from django.urls import path
from chat import consumers

websocket_urlpatterns = [
    path('ws/chat/<int:chat_id>/', consumers.ChatConsumer.as_asgi()),
]
