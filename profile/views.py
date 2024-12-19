"""
This module defines the views for the profile app.

Views:
    - signup
    - profile
    - subscribe
    - unsubscribe
    - subscribers_page
    - subscribed_page
"""

from profile.models import Profile
from profile.forms import RegisterForm, ProfileForm

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.http import HttpResponseRedirect
from django.urls import reverse

from news.models import Post
from news.forms import PostForm

def signup(request):
    """
    Displays the signup page and renders the signup form.

    Returns:
        HttpResponse: Renders the signup page and form.
    """
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        profile_form = ProfileForm(request.POST)
        if form.is_valid() and profile_form.is_valid():
            user = form.save()
            profile = profile_form.save(commit = False)
            profile.user = user
            profile.save()
            return redirect('/login/')
    else:
        form = RegisterForm()

    return render(request, 'registration/signup.html', {'form': form})


def profile(request, username):
    """
    Displays the profile page, posts, subscribers, unsubscribed and subscription status.

    Returns:
        HttpResponse: Renders the profile page.
    """
    User = get_user_model()
    user = User.objects.get(username = username)
    posts = Post.objects.filter(author = user.id).order_by('-date')
    profile = user.profile
    is_subscribed = request.user.profile.subscription.filter(
        user = user).exists() if request.user.is_authenticated else False
    subscribed = profile.subscription.all()
    subscribers = Profile.objects.filter(subscription = user.profile)
    subscribers_count = subscribers.count()
    subscribed_count = subscribed.count()

    if request.method == "POST":
        if 'subscribe' in request.POST:
            subscriber = request.user.profile
            profile.subscription.add(subscriber)
        elif 'unsubscribe' in request.POST:
            subscriber = request.user.profile
            profile.subscription.remove(subscriber)

    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit = False)
            post.author = request.user
            post.save()
            return HttpResponseRedirect(reverse('profile', args = [request.user.username]))

    return render(
        request,
        "profile/profile.html",
        {
            'username': user.username,
            'profile_pic': profile.profile_pic.url,
            'description': profile.description,
            'posts': posts,
            'is_subscribed': is_subscribed,
            'subscribers': subscribers,
            'subscribed': subscribed,
            'subscribers_count': subscribers_count,
            'subscribed_count': subscribed_count,
        }
    )

@login_required
def subscribe(request, username):
    """
    Allows the logged-in user to subscribe to profile.

    Returns:
        JsonResponse: Json response with success.
    """
    User = get_user_model()
    user_to_subscribe = User.objects.get(username=username)
    request.user.profile.subscription.add(user_to_subscribe.profile)

    return JsonResponse({
        'success': True,
        'username': user_to_subscribe.username
    })

@login_required
def unsubscribe(request, username):
    """
    Allows the logged-in user to unsubscribe from profile.

    Returns:
        JsonResponse: Json response with success.
    """
    User = get_user_model()
    user_to_unsubscribe = User.objects.get(username=username)
    request.user.profile.subscription.remove(user_to_unsubscribe.profile)

    return JsonResponse({
        'success': True,
        'username': user_to_unsubscribe.username
    })

@login_required
def subscribers_page(request, username):
    """
    Displays the subscribers page.

    Returns:
        HttpResponse: Renders the subscribers page.
    """
    User = get_user_model()
    user = get_object_or_404(User, username=username)
    user_profile = user.profile
    subscribers = Profile.objects.filter(subscription=user_profile)

    return render(
        request,
        'profile/subscribers.html',
        {
            'profile': user_profile,
            'subscribers': subscribers
        }
    )


@login_required
def subscribed_page(request, username):
    """
    Displays the subscribed page.

    Returns:
        HttpResponse: Renders the subscribed page.
    """
    User = get_user_model()
    user = get_object_or_404(User, username=username)
    user_profile = user.profile
    subscribed = user_profile.subscription.all()

    return render(
        request,
        'profile/subscribed.html',
        {
            'profile': user_profile,
            'subscribed': subscribed
        }
    )
