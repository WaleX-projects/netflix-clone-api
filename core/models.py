from django.db import models
from django.contrib.auth.models import User
import uuid

class Genre(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Movie(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    release_date = models.DateField()
    genres = models.ManyToManyField(Genre)
    thumbnail = models.ImageField(upload_to='thumbnails/')
    video_file = models.FileField(upload_to='movies/')
    uuid = models.UUIDField(default=uuid.uuid4, unique=True)
    
    def __str__(self):
        return self.title


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    profile_image = models.ImageField(upload_to='profiles/', null=True, blank=True)
    is_kids = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.name}"

class VideoHistory(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    watched_at = models.DateTimeField(auto_now_add=True)
    progress = models.IntegerField(default=0) # Seconds where user left off

class Watchlist(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    movies = models.ManyToManyField(Movie)

# Create your models here.
