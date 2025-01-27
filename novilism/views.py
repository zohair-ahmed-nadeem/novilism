from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, logout
from .forms import CustomLoginForm, CustomRegisterForm
from post.models import Profile , Post, Notification, WebsiteUpdate
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from post.forms import PostForm
from django.http import JsonResponse
from post.models import Notification
from django.http import HttpResponse
from django.urls import reverse

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

def home(request):
    tag = request.GET.get('tag')
    if tag:
        posts = Post.objects.filter(tags=tag)
    else:
        posts = Post.objects.all()
    return render(request, 'website/index.html', {'posts': posts, 'tag': tag})


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

def about(request):
    return render(request, 'website/about.html')

def get_notifications(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    website_updates = WebsiteUpdate.objects.order_by('-created_at')

    notification_data = [{
        'id': n.id,
        'type': 'comment',
        'post_title': n.post.title,
        'comment_content': n.comment.content,
        'is_read': n.is_read,
        'comment_author': n.comment.user.username,
    } for n in notifications]

    update_data = [{
        'id': update.id,
        'type': 'update',
        'title': update.title,
        'content': update.content,
        'created_at': update.created_at.strftime('%Y-%m-%d %H:%M:%S'),
    } for update in website_updates]

    # Combine comment and update notifications
    all_notifications = notification_data + update_data

    # Sort by created_at (for updates) and `created_at` assumed in Notification
    sorted_notifications = sorted(all_notifications, key=lambda x: x.get('created_at', ''), reverse=True)

    return JsonResponse(sorted_notifications, safe=False)


def mark_as_read(request, id):
    notification = Notification.objects.get(id=id)
    notification.is_read = True
    notification.save()
    return HttpResponse(status=204)

def delete_notification(request, notification_id):
    try:
        notification = Notification.objects.get(id=notification_id)
        notification.delete()
        return JsonResponse({'success': True})
    except Notification.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Notification not found'}, status=404)


def fule (request):
    return render(request, 'website/fule.html')

