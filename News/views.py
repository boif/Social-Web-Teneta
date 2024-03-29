from django.shortcuts import render, redirect
from django.views.generic import DetailView, UpdateView, DeleteView
from News.models import *
from News.forms import PostForm
from django.http import JsonResponse
from django.views.decorators.http import require_POST
def createPost(request):
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
    return render(request, 'home.html', {'posts': posts, 'form': form})

class PostDetailView(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'

class PostUpdateView(UpdateView):
    model = Post
    template_name = 'post_update.html'
    fields = ['text', 'content']

class PostDeleteView(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = '/'

@require_POST
def like_post(request, post_id):
    post = Post.objects.get(pk=post_id)
    like, created = Like.objects.get_or_create(user=request.user, post=post)
    if not created:
        like.delete()
    return JsonResponse({'likes': post.likes.count()})

@require_POST
def add_comment(request, post_id):
    post = Post.objects.get(pk=post_id)
    text = request.POST.get('text')
    Comment.objects.create(user=request.user, post=post, text=text)
    return JsonResponse({'success': True})