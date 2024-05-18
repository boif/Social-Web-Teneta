from django.shortcuts import render, redirect
from Profile.forms import RegisterForm, ProfileForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from News.models import Post
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
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit = False)
            post.author = request.user
            post.save()
            return HttpResponseRedirect(reverse('profile', args = [request.user.username]))
    return render(
        request,
        "profile.html",
        {
            'username': user.username,
            'profile_pic': profile.profile_pic.url,
            'description': profile.description,
            'posts': posts,
            'is_subscribed': is_subscribed
        }
    )

@login_required
def subscribe(request, username):
    user_to_subscribe = User.objects.get(username=username)
    request.user.profile.subscription.add(user_to_subscribe.profile)
    return JsonResponse({'success': True})

@login_required
def unsubscribe(request, username):
    user_to_unsubscribe = User.objects.get(username=username)
    request.user.profile.subscription.remove(user_to_unsubscribe.profile)
    return JsonResponse({'success': True})