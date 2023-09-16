from django.contrib.auth import get_user_model
from django.contrib.humanize.templatetags.humanize import naturaltime, naturalday
from django.db import models
from django.conf import settings

User = get_user_model()

# Create your models here.


class Post(models.Model):
    title = models.CharField(max_length=30, blank=True)
    content = models.CharField(max_length=512, blank=True)
    created = models.DateTimeField(auto_now_add=True, blank=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    image = models.ImageField(blank=True, null=True, upload_to='post_images')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('created',)


class Like(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, null=True, blank=True, related_name='liked_posts')
    post = models.ForeignKey(to=Post, on_delete=models.CASCADE, null=True, blank=True, related_name='likes')


class Comment(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='commented_posts', null=True, blank=True)
    post = models.ForeignKey(to=Post, on_delete=models.CASCADE, related_name='comments', null=True, blank=True)
    text = models.CharField(max_length=100, null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} {self.id}'