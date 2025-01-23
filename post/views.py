from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from post.models import Post, Comment
from post.forms import PostForm , ProfileForm


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
    return render(request, 'website/index.html', {'posts': posts, 'tag': tag})


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
