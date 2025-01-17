from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Profile, Account
from django.conf import settings

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance)

@receiver(post_save, sender=Account)
def save_user_profile(sender, instance, **kwargs):

    if hasattr(instance, 'profile'):
        instance.profile.save()
