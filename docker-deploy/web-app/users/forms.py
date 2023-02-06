from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Profile


class CreateUserForm(UserCreationForm):
  class Meta:
    model = User
    fields = ['username', 'email', 'password1', 'password2']
    
class UserNameForm(forms.ModelForm):
  class Meta:
    model = User
    fields = ['username', 'email']

class ProfileForm(forms.ModelForm):
  class Meta:
    model = Profile
    fields = ['vehicle_type', 'license_plate', 'max_passengers','special_info']