from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import Post
from post.forms import PostForm
from django.shortcuts import render, get_object_or_404

def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = PostForm()
    return render(request, 'website/post.html', {'form': form})

def home(request):
    posts = Post.objects.all()
    return render(request, 'website/index.html', {'posts': posts})

def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    return render(request, 'website/post_detail.html', {'post': post})

# Edit Post
@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.user != request.user:
        return HttpResponseForbidden("You are not allowed to edit this post.")
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', post_id=post.id)
    else:
        form = PostForm(instance=post)
    return render(request, 'edit_post.html', {'form': form})

# Delete Post
@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.user != request.user:
        return HttpResponseForbidden("You are not allowed to delete this post.")
    post.delete()
    return redirect('index')
