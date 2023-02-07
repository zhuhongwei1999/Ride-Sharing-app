from django.contrib import admin
from .models import RideRequest, SearchRequest
# Register your models here.
admin.site.register(RideRequest)
admin.site.register(SearchRequest)