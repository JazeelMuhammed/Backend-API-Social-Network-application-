from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.auth.models import AbstractUser

User = get_user_model()

# rest framework


# Create your models here.

class ConnectionStatus:
    pending = 'PENDING'
    accepted = 'ACCEPTED'
    rejected = 'REJECTED'

USER_CHOICES = (
    (ConnectionStatus.pending, 'PENDING'),
    (ConnectionStatus.accepted, 'ACCEPTED'),
    (ConnectionStatus.rejected, 'REJECTED')
)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    bio = models.CharField(max_length=100, null=True, blank=True)
    location = models.CharField(max_length=100, null=True, blank=True)
    profile_picture = models.ImageField(upload_to="profile-pictures", null=True, blank=True)
    private = models.BooleanField(default=False)

    def get_user_id(self):
        return self.user.pk

    def get_username(self):
        return self.user.username

    def __str__(self):
        return self.user.username + ' profile'

    def delete_user(self):
        self.user.delete()


class Follow(models.Model):
    follower = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='follower', null=True, blank=True)
    following = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='following', null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return f'{self.follower} follows {self.following}'


class Connection(models.Model):
    sender = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='sender', null=True, blank=True)
    receiver = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='receiver', null=True, blank=True)
    status = models.CharField(max_length=20, choices=USER_CHOICES, default=ConnectionStatus.pending)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return f'Connection request from {self.sender} to {self.receiver}'




