from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

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
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)  # Temporarily set default user ID
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='images/')
    post_date = models.DateTimeField(default=timezone.now)
    tags = models.CharField(max_length=1, choices=STORY_TYPES, default='G')
    
    def __str__(self):
        return self.title

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='pfp/', default='default.jpg')

    def __str__(self):
        return self.user.username