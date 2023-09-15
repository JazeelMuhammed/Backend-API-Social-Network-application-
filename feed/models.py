from django.contrib.auth import get_user_model
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

