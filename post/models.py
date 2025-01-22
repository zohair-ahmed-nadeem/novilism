from django.db import models
from django.utils import timezone

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
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='media/images/')
    post_date = models.DateTimeField(default=timezone.now)
    tags = models.CharField(max_length=1, choices=STORY_TYPES, default='G')
    
    def __str__(self):
        return self.title
