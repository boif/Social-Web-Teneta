from django import forms
from Chat.models import Chat
from Chat.models import Message

class ChatForm(forms.ModelForm):
    class Meta:
        model = Chat
        fields = ['name', 'participants']
        widgets = {
            'participants': forms.CheckboxSelectMultiple,
        }

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['text']

