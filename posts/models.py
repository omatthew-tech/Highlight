from django.db import models
from django.contrib.auth.models import User
from django.db import models

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
    friends = models.ManyToManyField('self', blank=True)

    def are_friends(self, user):
        return user in self.friends.all()

class FriendRequest(models.Model):
    from_user = models.ForeignKey(User, related_name='outgoing_friend_requests', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='incoming_friend_requests', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)  # time of creation
    status = models.IntegerField(choices=(
        (0, 'Pending'),
        (1, 'Accepted'),
        (2, 'Declined'),
    ), default=0)

    class Meta:
        unique_together = ('from_user', 'to_user')

