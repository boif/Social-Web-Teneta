from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Chat, Message
from .forms import ChatForm, MessageForm


@login_required
def start_chat(request, username):
    other_user = get_object_or_404(User, username = username)

    chat = Chat.objects.filter(is_group_chat = False, participants = request.user).filter(
        participants = other_user).first()

    if not chat:
        chat = Chat.objects.create(is_group_chat = False)
        chat.participants.add(request.user, other_user)

    return redirect('chat_detail', chat_id = chat.id)


@login_required
def chat_detail(request, chat_id):
    chat = get_object_or_404(Chat, id = chat_id)

    # Exclude the current user from the participants to find the chat partner
    chat_partner = chat.participants.exclude(username = request.user.username).first()

    # Fetch the chat messages
    messages = Message.objects.filter(chat = chat).order_by('timestamp')

    return render(
        request,
        'chat/chat_detail.html',
        {
            'chat': chat,
            'chat_partner': chat_partner,
            'messages': messages
        }
    )