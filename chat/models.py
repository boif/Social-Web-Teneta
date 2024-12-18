"""
This module defines the models used in the chat app.

Models:
    - Chat
    - Message
"""

from django.db import models
from django.contrib.auth.models import User

class Chat(models.Model):
    """
    Represents a chat room.
    """
    is_group_chat = models.BooleanField(default=False)
    name = models.CharField(max_length=100, blank=True, null=True)
    participants = models.ManyToManyField(User, related_name='chats')

    def __str__(self):
        """
        Rerturn string representation of the chat room.
        """
        if self.is_group_chat:
            return f"Group Chat: {self.name}"
        else:
            return f"Chat between: {', '.join([user.username for user in self.participants.all()])}"

class Message(models.Model):
    """
    Represents a message sent in a chat room.
    """
    chat = models.ForeignKey(Chat, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        Return a string representation of the message.
        """
        return f"Message from {self.sender.username} in {self.chat}"
