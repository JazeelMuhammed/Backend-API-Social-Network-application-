from django.contrib.auth import get_user_model
from .models import UserProfile
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import UserProfile

User = get_user_model()


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    # When we are saving a user for the 1st time, created argument will be True
    if created:
        UserProfile.objects.create(
            user=instance
        )