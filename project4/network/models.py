from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    following = models.ManyToManyField("self", symmetrical=False, blank=True, related_name="followers")

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    content = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    followers = models.ManyToManyField(User, blank=True, related_name="followed_posts")

    def __str__(self):
        return f"{self.user} posted {self.content} at {self.timestamp}"
