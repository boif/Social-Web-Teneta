from django import forms
from django.contrib.auth.models import User
from Chat.models import Message

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']
        widgets = {
            'content': forms.Textarea(
                attrs={'placeholder': 'Введите сообщение...', 'rows': 3}
            ),
        }

class ChatForm(forms.Form):
    user = forms.ModelChoiceField(
        queryset=User.objects.all(),
        widget=forms.Select(
            attrs={'class': 'form-control'}
        )
    )
