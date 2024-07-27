from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Chat, Message
from .forms import ChatForm, MessageForm

@login_required
def create_chat(request):
    if request.method == 'POST':
        form = ChatForm(request.POST)
        if form.is_valid():
            chat = form.save()
            chat.participants.add(request.user)  # Add current user to chat participants
            chat.save()
            return redirect('chat_detail', chat_id=chat.id)
    else:
        form = ChatForm()

    return render(request, 'chat/create_chat.html', {'form': form})

@login_required
def chat_detail(request, chat_id):
    chat = get_object_or_404(Chat, id=chat_id)

    # Ensure the user is a participant in the chat
    if request.user not in chat.participants.all():
        return redirect('home')

    messages = chat.messages.all().order_by('created_at')

    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.chat = chat
            message.save()
            return redirect('chat_detail', chat_id=chat.id)
    else:
        form = MessageForm()

    return render(request, 'chat/chat_detail.html', {
        'chat': chat,
        'messages': messages,
        'form': form
    })