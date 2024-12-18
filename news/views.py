from django.shortcuts import render, redirect
from django.views.generic import DetailView, UpdateView, DeleteView
from news.models import *
from news.forms import PostForm
from django.http import JsonResponse
from django.views.decorators.http import require_POST

"""
This module defines the views for the news app.

views:
    - createPost
    - PostDetailView
    - PostUpdateView
    - PostDeleteView
    - likePost
    - addComment
"""

def createPost(request):
    """
    Handles the creation of a new post.

    Returns:
        HttpResponse: Renders the home page with the form and list of posts.
    """
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('/')
    else:
        form = PostForm()
    posts = Post.objects.all().order_by('-date')
    return render(
        request,
        'home.html',
        {'posts': posts, 'form': form}
    )

class PostDetailView(DetailView):
    """
    Displays the details of the post.
    """
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'

class PostUpdateView(UpdateView):
    """
    Handles the updating of the post.
    """
    model = Post
    template_name = 'post_update.html'
    fields = ['text', 'content']

class PostDeleteView(DeleteView):
    """
    Handles the deletion of the post.
    """
    model = Post
    template_name = 'post_delete.html'
    success_url = '/'

@require_POST
def likePost(request, post_id):
    """
    Handles liking and unliking the post.

    Returns:
        JsonResponse: Returns the updated number of likes for the post
    """
    post = Post.objects.get(pk=post_id)
    like, created = Like.objects.get_or_create(user=request.user, post=post)
    if not created:
        like.delete()
    return JsonResponse({'likes': post.likes.count()})

@require_POST
def CommentPost(request, post_id):
    """
    Handles commenting on the post.

    Returns:
        JsonResponse: Indicates the comment was successfully added.
    """
    post = Post.objects.get(pk=post_id)
    text = request.POST.get('text')
    Comment.objects.create(user=request.user, post=post, text=text)
    return JsonResponse({'success': True})
