from django.urls import path
from . import views

urlpatterns = [
    path('get_clothes/', views.get_clothes, name='get_clothes'),
    path('get_clothes/<str:pk>/', views.get_cloth, name='get_clothes'),
    path('search_clothes/', views.search_clothes, name='search_clothes'),
]