from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from accounts.models import UserProfile, UserInterest
from core.constants import DEFAULT_INTERESTS
import logging

logger = logging.getLogger(__name__)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Signal to create user profile when user is created
    """
    if created:
        profile = UserProfile.objects.create(user=instance)
        logger.info(f'Created profile for user: {instance.username}')
        
        # Add default interests
        for interest_name in DEFAULT_INTERESTS:
            UserInterest.objects.create(
                profile=profile,
                name=interest_name
            )
        logger.info(f'Added default interests for user: {instance.username}')


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """
    Signal to save user profile when user is saved
    """
    if hasattr(instance, 'profile'):
        instance.profile.save()
