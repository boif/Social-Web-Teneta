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
    posts = Post.objects.filter(author=user.id)
    profile = user.profile
    return render(
        request,
        "profile.html",
        {
            'username': user.username,
            'profile_pic': profile.profile_pic.url,
            'description': profile.description,
            'posts': posts
        }
    )

@login_required()
def subscribe(request, user_id):
    if request.method == 'POST':
        subscribed_to_user = Subscription.objects.get(pk=user_id)
        Subscription.objects.create(user=request.user, subscribe_to=subscribed_to_user)
        return redirect('profile', user_id=user_id)
    return redirect('home')

@login_required()
def unsubscribe(request, user_id):
    if request.method == 'POST':
        subscribed_from_user = Subscription.objects.get(pk=user_id)
        Subscription.objects.filter(user=subscribed_from_user, subscribe_to=subscribed_from_user).delete()
        return redirect('profile', user_id=user_id)
    return redirect('home')
