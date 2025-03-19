from django.urls import path
from .views import ShipmentCreateView, ShipmentStatusView, ShipmentDetailView

urlpatterns = [
    path('create/', ShipmentCreateView.as_view(), name='shipment-create'),
    # path('detail/<int:pk>/', ShipmentStatusView.as_view(), name='shipment-detail'),
    path('detail/<int:id>/', ShipmentDetailView.as_view(), name='shipment_detail'),
]
