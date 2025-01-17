from django.shortcuts import render,redirect
from .models import Post
from post.forms import PostForm

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