from django.urls import path
from .views import OrderItemListView, OrderListByStatus, AddToOrderView, OrderDetailView

urlpatterns = [
    path('all/', OrderItemListView.as_view(), name='order_item_list'),
    path('all/status/', OrderListByStatus.as_view(), name='order_list_by_status'),
    path('add_to_order/', AddToOrderView.as_view(), name='add_to_order'),
    path('detail/<int:order_item_id>/',OrderDetailView.as_view(), name='order_item_view'),
]
