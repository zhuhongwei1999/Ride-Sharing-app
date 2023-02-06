from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import RideRequest

@receiver(post_save, sender=User)
def create_request(sender, instance, created, **kwargs):
  if created:
    RideRequest.objects.create(user=instance)