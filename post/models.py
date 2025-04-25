from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from markdownx.models import MarkdownxField

class Post(models.Model):
    STORY_TYPES = (
        ('F', 'Fiction'),
        ('N', 'Non-Fiction'),
        ('P', 'Poetry'),
        ('R', 'Romantic'),
        ('H', 'Horror'),
        ('S', 'Science Fiction'),
        ('M', 'Mystery'),
        ('C', 'Comedy'),
        ('D', 'Drama'),
        ('A', 'Action'),
        ('T', 'Thriller'),
        ('G', 'General'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = MarkdownxField()
    image = models.ImageField(upload_to='images/')
    post_date = models.DateTimeField(default=timezone.now)
    tags = models.CharField(max_length=1, choices=STORY_TYPES, default='G')
    view_count = models.PositiveIntegerField(default=0)
    likes = models.ManyToManyField(User, related_name='post_likes', blank=True)


    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.user.username} on {self.post.title}'

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='pfp/', blank=True, null=True)

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created and not hasattr(instance, 'profile'):
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
    
class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    email = models.EmailField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.email and self.user:
            self.email = self.user.email
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Feedback from {self.user.username if self.user else "Anonymous"} on {self.created_at}'
    
class Collaborator(models.Model):
    name = models.CharField(max_length=100)
    profile_picture = models.ImageField(upload_to='collaborators/')
    profile_link = models.URLField()

    def __str__(self):
        return self.name

class Report(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='reports')
    reason = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    post_owner_email = models.EmailField(blank=True, null=True)
    reporter_email = models.EmailField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.post_owner_email:
            self.post_owner_email = self.post.user.email
        if not self.reporter_email:
            self.reporter_email = self.user.email
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Report by {self.user.username} on {self.post.title}'

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

class WebsiteUpdate(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
