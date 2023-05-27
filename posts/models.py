from django.db import models
from django.contrib.auth.models import User
from django.db import models

class Post(models.Model):
    text = models.TextField()
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    # Other fields as per your requirements...

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    location = models.CharField(max_length=30, blank=True)
    bio = models.TextField(blank=True)
