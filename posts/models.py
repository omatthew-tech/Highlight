from django.db import models
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    text = models.TextField()
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    likes = models.ManyToManyField(User, related_name='likes', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile_pics/', default='profile_pics/ProfilePic.jpg', blank=True)
    location = models.CharField(max_length=30, blank=True)
    bio = models.TextField(blank=True)
    friends = models.ManyToManyField("self")
    last_post_time = models.DateTimeField(default=timezone.now)

    def friend_requests(self):
        return self.to_friend.filter(status='pending')

    def add_friend(self, profile):
        self.friends.add(profile)

class FriendRequest(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    )

    from_profile = models.ForeignKey(Profile, related_name='from_friends', on_delete=models.CASCADE)
    to_profile = models.ForeignKey(Profile, related_name='to_friends', on_delete=models.CASCADE)
    status = models.CharField(choices=STATUS_CHOICES, max_length=10, default='pending')

