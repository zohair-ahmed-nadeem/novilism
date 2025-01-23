from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from post.models import Post, Comment, Collaborator
from post.forms import PostForm , ProfileForm, FeedbackForm, ReportForm
from django.db.models import Count
import random
from django.http import JsonResponse


@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('post_detail', post_id=post.id)
    else:
        form = PostForm()
    return render(request, 'website/post.html', {'form': form})

def home(request):
    tag = request.GET.get('tag')
    if tag:
        posts = Post.objects.filter(tags=tag)
    else:
        posts = Post.objects.all()

    top_viewed_posts = Post.objects.order_by('-view_count')[:5]
    top_liked_posts = Post.objects.annotate(like_count=Count('likes')).order_by('-like_count')[:5]
    recent_posts = Post.objects.order_by('-post_date')[:5]
    collaborators = Collaborator.objects.all()

    # Get random posts excluding the ones already selected
    selected_posts_ids = set(post.id for post in top_viewed_posts) | set(post.id for post in top_liked_posts) | set(post.id for post in recent_posts)
    random_posts = Post.objects.exclude(id__in=selected_posts_ids)
    random_posts = random.sample(list(random_posts), min(len(random_posts), 5))

    return render(request, 'website/index.html', {
        'posts': posts,
        'tag': tag,
        'top_viewed_posts': top_viewed_posts,
        'top_liked_posts': top_liked_posts,
        'recent_posts': recent_posts,
        'random_posts': random_posts,
        'collaborators': collaborators,
    })


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post.view_count += 1
    post.save()
    return render(request, 'website/post_detail.html', {'post': post})

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


@login_required
def like_post_view(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return redirect('post_detail', post_id=post.id)

@login_required
def add_comment_view(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Comment.objects.create(post=post, user=request.user, content=content)
    return redirect('post_detail', post_id=post.id)

@login_required
def edit_profile_view(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'website/profile.html', {'form': form})

@login_required
def feedback_view(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.user = request.user
            feedback.save()
            return redirect('home')
    else:
        form = FeedbackForm()
    return render(request, 'website/feedback.html', {'form': form})

def collaborators_view(request):
    collaborators = Collaborator.objects.all()
    return render(request, 'website/collaborators.html', {'collaborators': collaborators})

def report_post_view(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.user = request.user
            report.post = post
            report.save()
            return redirect('post_detail', post_id=post.id)
    else:
        form = ReportForm()
    return render(request, 'website/report_post.html', {'form': form, 'post': post})

def search_posts(request):
    if 'q' in request.GET:
        query = request.GET.get('q')
        posts = Post.objects.filter(title__icontains=query).values('id', 'title')
        return JsonResponse(list(posts), safe=False)
    return JsonResponse([], safe=False)