import logging

from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings
from .models import Profiles


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_new_profile(sender, instance, created, **kwargs):
    if created:
        # using current User Model instance to create a new Profile obj with default values
        Profiles.objects.create(user=instance)
        instance.profile.save()  # saving the Profile obj previously created for the current user instance
        logging.info(f"{instance}'s base profile is created.")
    
    else : logging.info("Profile status is saved")
