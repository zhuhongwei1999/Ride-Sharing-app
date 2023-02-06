from django import forms
from .models import RideRequest,SearchRequest
import datetime
from django.core.exceptions import ValidationError
import pytz
from django.conf import settings

class SearchForm(forms.ModelForm):
  class Meta:
    model = SearchRequest
    fields = ['destination',
              'earlydate',
              'earlytime',
              'latedate',
              'latetime',
              'seats_needed',]
    widgets = {
      'earlydate': forms.DateInput(attrs={'type': 'date'}),
      'earlytime': forms.TimeInput(attrs={'type': 'time'}),
      'latedate': forms.DateInput(attrs={'type': 'date'}),
      'latetime': forms.TimeInput(attrs={'type': 'time'}),
    }
    
    
class RideRequestForm(forms.ModelForm):
  class Meta:
    model = RideRequest
    fields = ['origin', 
              'destination', 
              'date', 
              'time', 
              'seats_needed',
              'can_be_shared',
              'required_type',
              'special_requirement',]
    widgets = {
      'date': forms.DateInput(attrs={'type': 'date'}),
      'time': forms.TimeInput(attrs={'type': 'time'}),
    }
    
  def clean(self):
    cleaned_data = super().clean()
    date = cleaned_data.get('date')
    time = cleaned_data.get('time')
    if date and time:
      tz = pytz.timezone(settings.TIME_ZONE)
      now = tz.localize(datetime.datetime.now())
      min_datetime = datetime.datetime.combine(now.date(), now.time())
      input_datetime = datetime.datetime.combine(date, time)
      if input_datetime < min_datetime:
        raise ValidationError("Date and time must not be earlier than the current date and time.")