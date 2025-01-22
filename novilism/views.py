from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, authenticate,logout
from .forms import CustomLoginForm, CustomRegisterForm
from post.models import Post

def login_view(request):
    if request.method == 'POST':
        form = CustomLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('home') 
    else:
        form = CustomLoginForm()

    return render(request, 'website/login.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        form = CustomRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
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
