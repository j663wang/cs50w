from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
    following = models.ManyToManyField("self", symmetrical=False, blank=True, related_name="followers")
    bio= models.CharField(max_length=500, blank=True)

    def __str__(self):
        return f"{self.username}" 