from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from post.models import Post, Comment, Collaborator, Profile
from post.forms import PostForm , ProfileForm, FeedbackForm, ReportForm
from django.db.models import Count
from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta


@login_required
def create_post(request):
    if request.method == 'POST':
        try:
            form = PostForm(request.POST, request.FILES)
            if form.is_valid():
                post = form.save(commit=False)
                post.user = request.user
                post.save()
                return redirect('post_detail', post_id=post.id)
        except Exception as e:
            form.add_error(None, f"Error creating post: {str(e)}")
    else:
        form = PostForm()
    return render(request, 'website/post.html', {'form': form})

def home(request):
    tag = request.GET.get('tag')
    
    # Filter posts by tag if provided
    if tag:
        posts = Post.objects.filter(tags__icontains=tag)  # Assuming `tags` is a CharField or use __name for related models
    else:
        posts = Post.objects.all()

    # Get current month range
    now = timezone.now()
    start_of_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    end_of_month = (start_of_month + timedelta(days=32)).replace(day=1)

    # Get top 5 posts by views, likes, and recent, each in descending order
    top_viewed_posts = Post.objects.order_by('-view_count')[:5]
    top_liked_posts = Post.objects.annotate(like_count=Count('likes')).order_by('-like_count')[:5]
    recent_posts = Post.objects.order_by('-post_date')[:5]

    # Ensure posts are in strict descending order (no ties)
    top_viewed_posts = sorted(top_viewed_posts, key=lambda p: p.view_count, reverse=True)
    top_liked_posts = sorted(top_liked_posts, key=lambda p: p.likes.count(), reverse=True)
    recent_posts = sorted(recent_posts, key=lambda p: p.post_date, reverse=True)

    # Get all collaborators
    collaborators = Collaborator.objects.all()

    # Get random posts excluding selected ones
    selected_posts_ids = set(post.id for post in top_viewed_posts) | set(post.id for post in top_liked_posts) | set(post.id for post in recent_posts)
    random_posts = Post.objects.exclude(id__in=list(selected_posts_ids)).order_by('?')[:5]

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
        posts = Post.objects.filter(title__icontains=query).values('id', 'title','user__username')
        return JsonResponse(list(posts), safe=False)
    return JsonResponse([], safe=False)

@login_required
def edit_profile_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile, user=request.user)
        name = request.POST.get('name')
        if form.is_valid():
            profile = form.save(commit=False)
            profile.name = name
            profile.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile, user=request.user)
    return render(request, 'website/profile.html', {'form': form})