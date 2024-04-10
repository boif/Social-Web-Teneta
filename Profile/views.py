from django.shortcuts import render, redirect
from Profile.forms import RegisterForm, ProfileForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from Profile.models import Subscription
from News.models import Post


def signup(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        profile_form = ProfileForm(request.POST)
        if form.is_valid() and profile_form.is_valid():
            user = form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            return redirect('/login/')
    else:
        form = RegisterForm()
    return render(
        request,
        'registration/signup.html',
        {
            'form': form,
        },
    )

def profile(request, username):
    user = User.objects.get(username=username)
    posts = Post.objects.filter(author=user)  # Убрано использование .id
    profile = user.profile
    is_subscribed = False  # По умолчанию не подписан
    if request.user.is_authenticated:
        is_subscribed = Subscription.objects.filter(user=request.user, subscribed_to=user).exists()
    return render(
        request,
        "profile.html",
        {
            'username': user.username,
            'profile_pic': profile.profile_pic.url,
            'description': profile.description,
            'posts': posts,
            'is_subscribed': is_subscribed,
        }
    )

@login_required()
def subscribe(request, username):
    if request.method == 'POST':
        subscribed_to_user = User.objects.get(username=username)
        Subscription.objects.create(user=request.user, subscribed_to=subscribed_to_user)
        return redirect('profile', username=subscribed_to_user.username)
    return redirect('home')

@login_required()
def unsubscribe(request, username):
    if request.method == 'POST':
        subscribed_to_user = User.objects.get(username=username)
        Subscription.objects.filter(user=request.user, subscribed_to=subscribed_to_user).delete()
        return redirect('profile', username=subscribed_to_user.username)
    return redirect('home')