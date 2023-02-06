from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('', views.home, name='home'),
    path('ride-request/', views.submit_ride_request, name='ride-request'),
    path('show-request/', views.ride_requests_view, name='show-request'),
    path('edit-request/<int:pk>/', EditRideRequestView.as_view(), name='edit-request'),
    path('cancel-request/<int:pk>/', CancelRideRequestView.as_view(), name='cancel-request'),
    path('search-for-open-rides/',views.search_rides_driver,name='search-for-open-rides'), 
    path('view-comfirmed-rides/',views.comfirmed_rides_view_driver,name='view-comfirmed-rides'),
    path('comfirm-ride/<int:pk>/',ComfirmRideRequest.as_view(),name = 'comfirm-ride'),
    path('complete-ride/<int:pk>/',CompleteRide.as_view(),name = 'complete-ride'),
    path('search-for-open-rides-sharer/',views.search_rides_sharer,name='search-for-open-rides-sharer'), 
    path('view-shared-rides/',views.shared_rides_view_sharer,name='view-shared-rides'),
    path('join-ride/<int:pk>/',JoinRideRequest.as_view(),name = 'join-ride'),
    path('exit-request/<int:pk>/', ExitRideRequest.as_view(), name='exit-request'),
]