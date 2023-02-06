from django.contrib.auth.models import User
from django.db import models

VEHICLE_TYPE = (
  ('SEDAN', 'SEDAN'),
  ('SUV', 'SUV'),
  ('TRUCK', 'TRUCK'),
)

class Profile(models.Model):
  user = models.OneToOneField(User, null=True, on_delete = models.CASCADE)
  registered_driver = models.BooleanField(default=False)
  vehicle_type = models.CharField(max_length=20, choices=VEHICLE_TYPE)
  license_plate = models.CharField(max_length=20, default='', blank=True)
  max_passengers = models.CharField(max_length=2, default='', blank=True)
  special_info = models.TextField(blank=True, default='')
  
  def __str__(self) -> str:
    return self.user.username