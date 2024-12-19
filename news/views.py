"""
This module defines the views for the news app.

Views:
    - create_post
    - PostDetailView
    - PostUpdateView
    - PostDeleteView
    - like_post
    - comment_post
"""

from django.shortcuts import render, redirect
from django.views.generic import DetailView, UpdateView, DeleteView
from django.views.decorators.http import require_POST
from django.http import JsonResponse

from news.models import Post, Like, Comment  # Только необходимые импорты
from news.forms import PostForm

def create_post(request):
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
    posts = Post.objects.all().order_by('-date')  # pylint: disable=no-member
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
def like_post(request, post_id):
    """
    Handles liking and unliking the post.

    Returns:
        JsonResponse: Returns the updated number of likes for the post
    """
    post = Post.objects.get(pk=post_id)  # pylint: disable=no-member
    like, created = Like.objects.get_or_create(user=request.user, post=post)  # pylint: disable=no-member
    if not created:
        like.delete()
    return JsonResponse({'likes': post.likes.count()})

@require_POST
def comment_post(request, post_id):
    """
    Handles commenting on the post.

    Returns:
        JsonResponse: Indicates the comment was successfully added.
    """
    post = Post.objects.get(pk=post_id)  # pylint: disable=no-member
    text = request.POST.get('text')
    Comment.objects.create(user=request.user, post=post, text=text)  # pylint: disable=no-member
    return JsonResponse({'success': True})
