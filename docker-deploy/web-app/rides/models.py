from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from users import models as users_models
from django.db.models import CharField, Model
from django.contrib.postgres.fields import ArrayField
import datetime

RIDE_STATUS_CHOICES = [
    ('Open', 'Open'),
    ('Ongoing', 'Ongoing'),
    ('Completed', 'Completed'),
]
  
class RideRequest(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
  origin = models.CharField(max_length=100)
  destination = models.CharField(max_length=100)
  date_time = models.DateTimeField()
  seats_needed = models.PositiveSmallIntegerField()
  driver_name = models.CharField(default='', max_length=50, blank=True)
  driver_license = models.CharField(default='', max_length=50, blank=True)
  can_be_shared = models.BooleanField(default=False)
  share_name = ArrayField(
    models.CharField(max_length=50, null=True, blank=True),
    size=10,
    blank=True,
    null=True,
  )
  sharer_information = models.JSONField(default=dict, blank=True)
  required_type = models.CharField(max_length=20, choices=users_models.VEHICLE_TYPE, blank = True)
  special_requirement = models.TextField(blank=True, default='')
  created_at = models.DateTimeField(default=timezone.now)
  ride_status = models.CharField(max_length=10, choices=RIDE_STATUS_CHOICES, default='Open')
  current_passengers = models.SmallIntegerField(default=0)

  def __str__(self):
    return f"Ride from {self.origin} to {self.destination} on {self.date_time}"
  
  def get_absolute_url(self):
    return reverse('edit-request', kwargs={'pk': self.pk})


class SearchRequest(models.Model):
  # ride_request = models.ForeignKey(RideRequest, on_delete=models.CASCADE, null=True)
  user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
  destination = models.CharField(max_length=100)
  early_datetime = models.DateTimeField()
  late_datetime = models.DateTimeField()
  seats_needed = models.PositiveSmallIntegerField()
  
  def __str__(self):
    return f"Ride to {self.destination} between {self.early_datetime} and {self.late_datetime}"
  
  #def get_absolute_url(self):
  #  return reverse('edit-request', kwargs={'pk': self.pk})