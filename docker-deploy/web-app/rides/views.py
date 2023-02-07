from django.shortcuts import render, redirect, get_object_or_404
from .models import RideRequest,SearchRequest
from django.contrib.auth.decorators import login_required
from .forms import RideRequestForm,SearchForm
from django.contrib import messages
from django.views.generic import UpdateView
from django.views import View
from users.models import Profile
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import F
from django.db.models import Q
import datetime

# Create your views here.
def home(request):
  return render(request, 'users/home.html')

@login_required
def submit_ride_request(request):
  if request.method == 'POST':
    form = RideRequestForm(request.POST)
    if form.is_valid():
      ride_request = form.save(commit=False)
      ride_request.user = request.user
      ride_request.current_passengers = ride_request.seats_needed
      ride_request.save()
      messages.success(request, 'Ride is requested!')
      return redirect('/')
  else:
    form = RideRequestForm()
  context = {'form': form}
  return render(request, 'rides/submit_ride_request.html', context)

@login_required
def ride_requests_view(request):
  ride_requests = RideRequest.objects.filter(user=request.user)
  context = {'ride_requests': ride_requests}
  return render(request, 'rides/show_ride_requests.html', context)

  
@login_required
# Sharer: view shared rides
def shared_rides_view_sharer(request):
  ride_requests = RideRequest.objects.filter(share_name__contains = [request.user.username])
  context = {'ride_requests': ride_requests}
  return render(request, 'rides/view_shared_sharer.html', context)
  
@login_required
# Driver: view open rides
def search_rides_driver(request):
  user_profile = Profile.objects.get(user=request.user)
  if user_profile.registered_driver:
    driver = Profile.objects.filter(user=request.user).first()
    ride_requests = RideRequest.objects.filter(Q(special_requirement = driver.special_info) | Q(special_requirement = ''),
                                               Q(required_type = driver.vehicle_type)|Q(required_type = ''),
                                               ride_status = 'Open',
                                               current_passengers__lte = driver.max_passengers)
    ride_requests = ride_requests.exclude(share_name__contains = [request.user.username])
    
    #special request
    context = {'ride_requests': ride_requests}
    return render(request, 'rides/view_open_driver.html', context)

@login_required
# Driver: view comfirmed rides
def comfirmed_rides_view_driver(request):
  driver = Profile.objects.filter(user=request.user).first()
  ride_requests = RideRequest.objects.filter(driver_name = request.user.username)
  context = {'ride_requests': ride_requests}
  return render(request, 'rides/view_comfirmed_driver.html', context)

class EditRideRequestView(UpdateView):
  model = RideRequest
  template_name = 'rides/edit_ride_request.html'
  fields = [
    'origin',
    'destination',
    'date_time',
    'seats_needed',
    'can_be_shared',
    'required_type',
    'special_requirement',
  ]

  def get_object(self, queryset=None):
    return get_object_or_404(RideRequest, pk=self.kwargs['pk'])
  
  def form_valid(self, form):
    ride_request = form.save()
    sharer_info = ride_request.sharer_information
    sharer_names = list(sharer_info.keys())
    for sharer_name in sharer_names:
      email = sharer_info[sharer_name]['email']
      send_cancel_email(email, ride_request.__str__())
      del ride_request.sharer_information[sharer_name]
    ride_request.share_name = None
    ride_request.current_passengers = ride_request.seats_needed
    ride_request.save()
    messages.success(self.request, 'Ride request updated successfully!')
    return super().form_valid(form)

def send_cancel_email(user_email, request_details):
    subject = 'Ride Canceled'
    message = 'Dear Passengers,\n\nYour ride has been canceled due to changes made by the ride owner.\n\nDetails:\n' + request_details + '\n\nThank you for using our service.\n\nBest regards,\nSupport Team'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [user_email]
    send_mail(subject, message, email_from, recipient_list)

def send_confirmation_email(user_email, request_details):
    subject = 'Ride Confirmation'
    message = 'Dear Passengers,\n\nYour ride has been comfirmed.\n\nDetails:\n' + request_details + '\n\nThank you for using our service.\n\nBest regards,\nSupport Team'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [user_email]
    send_mail(subject, message, email_from, recipient_list)
    
class ComfirmRideRequest(View):
  def get(self, request, pk):
    ride_request = get_object_or_404(RideRequest, pk=pk)
    driver = Profile.objects.filter(user=request.user).first()
    ride_request.ride_status = 'Ongoing'
    ride_request.driver_name = request.user.username
    ride_request.driver_license = driver.license_plate
    if ride_request.required_type == '':
      ride_request.required_type = driver.vehicle_type
    ride_request.save()
    send_confirmation_email(ride_request.user.email, ride_request.__str__())
    for name in ride_request.share_name:
      email = ride_request.sharer_information[name]['email']
      send_confirmation_email(email, ride_request.__str__())   
    messages.success(request, 'You have successfully comfirmed the ride.')
    return redirect('/view-comfirmed-rides/')

class CompleteRide(View):
  def get(self, request, pk):
    ride_request = get_object_or_404(RideRequest, pk=pk)
    if ride_request.ride_status == 'Ongoing':
      ride_request.ride_status = 'Completed'
      ride_request.save()
      messages.success(request, 'You have successfully completed the ride.')
      return redirect('/view-comfirmed-rides/')


class CancelRideRequestView(View):
  def get(self, request, pk):
    ride_request = get_object_or_404(RideRequest, pk=pk)
    ride_request.delete()
    messages.success(request, 'The ride request has been successfully cancelled.')
    return redirect('/')
  
@login_required
# Sharer: search open rides
def search_rides_sharer(request):
  if request.method == 'POST':
    form = SearchForm(request.POST)
    if form.is_valid():
      search_request = form.save(commit=False)
      search_request.user = request.user
      search_request.save()
      ride_requests = RideRequest.objects.filter(ride_status = 'Open', 
                                                can_be_shared = True,
                                                destination = search_request.destination,
                                                date_time__range = (search_request.early_datetime, search_request.late_datetime),)
      ride_requests = ride_requests.exclude(share_name__contains = [request.user.username])
    context = {'form': form,'ride_requests': ride_requests, 'search_request': search_request}
    return render(request, 'rides/view_open_sharer.html', context)
  else:
    form = SearchForm()
    context = {'form': form}
    return render(request, 'rides/view_open_sharer.html', context)
  
class JoinRideRequest(View):
  def get(self, request, pk):
    ride_request = get_object_or_404(RideRequest, pk=pk)
    search_object = SearchRequest.objects.filter(user=request.user).last()
    sharer = Profile.objects.filter(user=request.user).first()
    if ride_request.share_name is None:
      ride_request.share_name = []
    ride_request.share_name.append(sharer.user.username)
    ride_request.current_passengers += search_object.seats_needed
    sharer_info = {sharer.user.username: {'email': sharer.user.email, 'seats_needed': search_object.seats_needed}}
    ride_request.sharer_information.update(sharer_info)
    ride_request.save()
    messages.success(request, 'You have successfully joined the ride.')
    return redirect('/view-shared-rides/')

class ExitRideRequest(View):
  def get(self, request, pk):
    ride_request = get_object_or_404(RideRequest, pk=pk)
    sharer = Profile.objects.filter(user=request.user).first()
    ride_request.current_passengers -= ride_request.sharer_information[sharer.user.username]['seats_needed']
    del ride_request.sharer_information[sharer.user.username]
    ride_request.share_name.remove(sharer.user.username)
    if ride_request.share_name == []:
      ride_request.share_name = None
    ride_request.save()
    messages.success(request, 'You have successfully exit this ride.')
    return redirect('/')