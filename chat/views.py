"""
This module defines the views for the chat app.
Views:
    - startChat
    - chatDetail
    - sendMessage
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from chat.models import Chat, Message
from django.views.decorators.http import require_POST
from django.http import JsonResponse

@login_required
def startChat(request, username):
    """
    Starts or retrieves a private chat between logged-in users.

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
def chatDetail(request, chat_id):
    """
    Displays a chat detail page.

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
def sendMessage(request, chat_id):
    """
    Send a message to a chat.

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
