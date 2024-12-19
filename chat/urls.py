"""
This module defines the url patterns for the chat app.

Routes:
    - 'chat/start/<str:username>/' : start new chat with user.
    - 'chat/<int:chat_id>/' : chat room.
    - 'chat/<int:chat_id>/send/' : send message to chat room.
"""

from django.urls import path
from chat import views

urlpatterns = [
    path('chat/start/<str:username>/', views.start_chat, name = 'start_chat'),
    path('chat/<int:chat_id>/', views.chat_detail, name = 'chat_detail'),
    path('chat/<int:chat_id>/send/', views.send_message, name='send_message'),
]