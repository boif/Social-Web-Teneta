"""
Views for chat app.
This module contains views for handling chats in the project.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from Chat.models import Chat, Message
from django.views.decorators.http import require_POST
from django.http import JsonResponse


@login_required
def start_chat(request, username):
    """
    Starts or retrieves a private chat between logged-in users.

    Args:
        request (HttpRequest): Request object.
        username (str): The username of the user to start a private chat.

    Returns:
        HttpResponse: Redirect to the private chat page.
    """
    other_user = get_object_or_404(User, username = username)
    chat = Chat.objects.filter(is_group_chat = False, participants = request.user).filter(
        participants = other_user).first()

    if not chat:
        chat = Chat.objects.create(is_group_chat = False)
        chat.participants.add(request.user, other_user)

    return redirect('chat_detail', chat_id = chat.id)


@login_required
def chat_detail(request, chat_id):
    """
    Displays a chat detail page.

    Args:
        request (HttpRequest): Request object.
        chat_id (int): The id of the chat room.

    Returns:
        HttpResponse: Redirect to the chat detail page.
    """
    chat = get_object_or_404(Chat, id = chat_id)
    chat_partner = chat.participants.exclude(username = request.user.username).first()
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


@login_required
@require_POST
def send_message(request, chat_id):
    """
    Send a message to a chat.

    Args:
        request (HttpRequest): Request object.
        chat_id (int): The id of the chat room where the message will be sent.

    Returns:
        JsonResponse: Json response indicating the success or failure.
    """
    chat = get_object_or_404(Chat, id = chat_id)
    message_content = request.POST.get('content')

    if message_content:
        Message.objects.create(
            chat = chat,
            sender = request.user,
            content = message_content
        )

    return JsonResponse({'success': True})
