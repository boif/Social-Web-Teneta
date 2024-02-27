from django.shortcuts import render, redirect
from .models import Profile, Message, Chat, Group, FriendRequest
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

def home(request):
    return render(request, 'home.html')

def news(request):
    return render(request, 'news.html')


@login_required
def profile_view(request):
    profile = request.user.profile
    friends = profile.friends.all()
    sent_requests = profile.friend_requests_sent.all()
    received_requests = profile.friend_requests_received.all()
    context = {
        'profile': profile,
        'friends': friends,
        'sent_requests': sent_requests,
        'received_requests': received_requests
    }
    return render(request, 'profile.html', context)

@login_required
def message_view(request, username):
    if request.method == 'POST':
        receiver = User.objects.get(username=username)
        sender = request.user
        text = request.POST['message']
        message = Message.objects.create(sender=sender, receiver=receiver, text=text)
        message.save()
        return redirect('message_view', username=username)
    else:
        receiver = User.objects.get(username=username)
        messages = Message.objects.filter(sender=request.user, receiver=receiver) | Message.objects.filter(sender=receiver, receiver=request.user)
        context = {
            'receiver': receiver,
            'messages': messages
        }
        return render(request, 'messages.html', context)

@login_required
def chat_view(request, chat_id):
    chat = Chat.objects.get(id=chat_id)
    if request.method == 'POST':
        text = request.POST['message']
        message = Message.objects.create(sender=request.user, receiver=chat.user, text=text)
        message.save()
        return redirect('chat_view', chat_id=chat_id)
    else:
        messages = Message.objects.filter(receiver=request.user, chat=chat)
        context = {
            'chat': chat,
            'messages': messages
        }
        return render(request, 'chat.html', context)

@login_required
def group_view(request, group_id):
    group = Group.objects.get(id=group_id)
    if request.method == 'POST':
        text = request.POST['message']
        message = Message.objects.create(sender=request.user, text=text)
        message.save()
        group.messages.add(message)
        return redirect('group_view', group_id=group_id)
    else:
        messages = group.messages.all()
        context = {
            'group': group,
            'messages': messages
        }
        return render(request, 'group.html', context)

@login_required
def friend_request_view(request):
    if request.method == 'POST':
        receiver_id = request.POST['receiver_id']
        receiver = Profile.objects.get(id=receiver_id)
        FriendRequest.objects.create(from_user=request.user.profile, to_user=receiver)
        return HttpResponse('Friend Request Sent!')
    else:
        return HttpResponse('Bad Request')