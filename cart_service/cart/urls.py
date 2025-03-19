from django.urls import path

from cart.views import CartView

urlpatterns = [
    path('', CartView.as_view(), name='cart'),
    path('add_to_cart/', CartView.as_view(), name='add_to_cart'),
    path('remove_from_cart/<int:cart_id>/', CartView.as_view(), name='remove_from_cart'),
    ]