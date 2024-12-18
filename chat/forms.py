from django import forms
from django.contrib.auth.models import User
from chat.models import Message

"""
This module defines the forms used in the chat app.
"""

class MessageForm(forms.ModelForm):
    """
    Form for creating and sending messages in the chat.
    """
    class Meta:
        model = Message
        fields = ['content']
        widgets = {
            'content': forms.Textarea(
                attrs={'placeholder': 'Введите сообщение...', 'rows': 3}
            ),
        }

class ChatForm(forms.Form):
    """
    Form for selecting a user to initiate a chat.
    """
    user = forms.ModelChoiceField(
        queryset=User.objects.all(),
        widget=forms.Select(
            attrs={'class': 'form-control'}
        )
    )
