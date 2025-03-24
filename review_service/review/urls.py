from django.urls import path
from .views import ReviewListView, ReviewCreateView, ReviewDetailView

urlpatterns = [
    path('reviews/', ReviewListView.as_view(), name='review_list'),
    path('reviews/create/', ReviewCreateView.as_view(), name='review_create'),
    path('reviews/<int:pk>/', ReviewDetailView.as_view(), name='review_detail'),
] 