from django.shortcuts import render, redirect , get_object_or_404
from Profile.forms import RegisterForm, ProfileForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from News.models import Post
from Profile.models import Profile
from News.forms import PostForm
from django.http import HttpResponseRedirect
from django.urls import reverse

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
    posts = Post.objects.filter(author=user.id).order_by('-date')
    profile = user.profile
    is_subscribed = request.user.profile.subscription.filter(user=user).exists() if request.user.is_authenticated else False
    subscribed = profile.subscription.all()
    subscribers = Profile.objects.filter(subscription = user.profile)
    subscribers_count = subscribers .count()
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
    user_to_subscribe = User.objects.get(username=username)
    request.user.profile.subscription.add(user_to_subscribe.profile)

    return JsonResponse({
        'success': True,
        'username': user_to_subscribe.username
    })

@login_required
def unsubscribe(request, username):
    user_to_unsubscribe = User.objects.get(username=username)
    request.user.profile.subscription.remove(user_to_unsubscribe.profile)

    return JsonResponse({
        'success': True,
        'username': user_to_unsubscribe.username
    })
@login_required
def subscribersPage(request, username):
    user = get_object_or_404(User, username=username)
    profile = user.profile
    subscribers = Profile.objects.filter(subscription = user.profile)

    return render(
        request,
        'profile/subscribers.html',
        {
            'profile': profile,
            'subscribers': subscribers
        }
    )


@login_required
def subscribesPage(request, username):
    user = get_object_or_404(User, username = username)
    profile = user.profile
    subscribes = profile.subscription.all()

    return render(
        request,
        'profile/subscribes.html',
        {
            'profile': profile,
            'subscribes': subscribes
        }
    )