from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from .forms import CreateUserForm, ProfileForm, UserNameForm
from django.contrib import messages
from django.http import HttpResponse
from .models import Profile
from django.contrib.auth.decorators import login_required

# Create your views here.
def register(request):
  if request.method == 'POST':
    form = CreateUserForm(request.POST)
    if form.is_valid():
      form.save()
      user = form.cleaned_data.get('username')
      messages.success(request, 'Account was created for' + user)
      return redirect('login')
  else:
    form = CreateUserForm()
  context = {'form': form}
  return render(request, 'users/register.html', context)

def log_in(request):
  if request.method == 'POST':
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
      login(request, user)
      return redirect('/')
    else:
      return render(request, 'users/login.html', {'error_message': 'Invalid login'})
  return render(request, 'users/login.html')
    
def log_out(request):
  logout(request)
  return redirect('/')

@login_required
def driver_update(request):
  if request.method == 'POST':
    profile_form = ProfileForm(request.POST, instance=request.user.profile)
    username_form = UserNameForm(request.POST, instance=request.user)
    if profile_form.is_valid() and username_form.is_valid():
      profile_form.save()
      username_form.save()
      messages.success(request, 'Your info has been updated!')
      return redirect('/')  
  else:
    profile_form = ProfileForm(instance=request.user.profile)
    username_form = UserNameForm(instance=request.user)
  context = {'profile_form': profile_form, 'username_form': username_form}
  return render(request, 'users/profile.html', context)

@login_required
def become_driver(request):
  user_profile = Profile.objects.get(user=request.user)
  if user_profile.registered_driver:
    messages.success(request, 'You have already registered as a driver, please update your information here!')
    return redirect('profile')
  if request.method == 'POST':
    profile_form = ProfileForm(request.POST, instance=request.user.profile)
    if profile_form.is_valid():
      request.user.profile.registered_driver = True
      request.user.profile.save()
      profile_form.save()
      messages.success(request, 'Now you are a driver!')
      return redirect('/')
  else:
    profile_form = ProfileForm(instance=request.user.profile)
  context = {'profile_form': profile_form}
  return render(request, 'users/driver.html', context)
  