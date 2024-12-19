"""
This module defines the forms used in the chat app.
"""

from django import forms
from django.contrib.auth import get_user_model
from chat.models import Message

class MessageForm(forms.ModelForm):
    """
    Form for creating and sending messages in the chat.
    """
    class Meta:
        """
        Meta options for the MessageForm.
        """
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
    User = get_user_model()
    user = forms.ModelChoiceField(
        queryset=User.objects.all(),
        widget=forms.Select(
            attrs={'class': 'form-control'}
        )
    )
