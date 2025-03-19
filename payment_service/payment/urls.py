from django.urls import path
from .views import CreatePaymentView

urlpatterns = [
    path('create/', CreatePaymentView.as_view(), name='create_payment'),
]
