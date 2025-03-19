
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('api/shipment_service/', include('ship_status.urls')),
]
