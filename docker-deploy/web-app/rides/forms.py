from django import forms
from .models import RideRequest,SearchRequest
from datetime import datetime
from django.core.exceptions import ValidationError
import pytz
from django.conf import settings
from django.utils import timezone

class SearchForm(forms.ModelForm):
  class Meta:
    model = SearchRequest
    fields = ['destination',
              'early_datetime',
              'late_datetime',
              'seats_needed',]
    widgets = {
      'early_datetime': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
      'late_datetime': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
    }
    
    
class RideRequestForm(forms.ModelForm):
  class Meta:
    model = RideRequest
    fields = ['origin', 
              'destination', 
              'date_time',
              'seats_needed',
              'can_be_shared',
              'required_type',
              'special_requirement',]
    widgets = {
      'date_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
    }
    
  def clean(self):
    date_time = self.cleaned_data['date_time']
    tz = pytz.timezone(settings.TIME_ZONE)
    now = timezone.now().astimezone(tz)
    if date_time <= now:
      raise ValidationError("Date and time must be in the future.")