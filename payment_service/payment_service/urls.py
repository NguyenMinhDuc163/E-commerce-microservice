from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('api/payment_service/', include('payment.urls')),
]
