from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, logout
from .forms import CustomLoginForm, CustomRegisterForm
from post.models import Profile , Post
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from post.forms import PostForm

def login_view(request):
    if request.method == 'POST':
        form = CustomLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if not hasattr(user, 'profile'):
                Profile.objects.create(user=user)
            auth_login(request, user)
            return redirect('home') 
    else:
        form = CustomLoginForm()

    return render(request, 'website/login.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        form = CustomRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            profile_picture = form.cleaned_data.get('profile_picture')
            if profile_picture:
                profile = Profile.objects.get(user=user)
                profile.profile_picture = profile_picture
                profile.save()
            auth_login(request, user)
            return redirect('home')
    else:
        form = CustomRegisterForm()

    return render(request, 'website/register.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

def h(request):
    posts = Post.objects.all()
    return render(request, 'website/index.html', {'posts': posts})

@login_required
def edit_post_view(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.user != request.user:
        return redirect('home')
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', post_id=post.id)
    else:
        form = PostForm(instance=post)
    return render(request, 'website/edit_post.html', {'form': form})

@login_required
def delete_post_view(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.user == request.user:
        post.delete()
    return redirect('home')