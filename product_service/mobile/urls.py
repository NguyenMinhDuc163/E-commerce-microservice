from django.urls import path
from . import views

urlpatterns = [
    path('get_mobiles/', views.get_mobiles, name='get_mobiles'),
    path('get_mobile/<str:pk>/', views.get_mobile, name='get_mobile'),
    path('search_mobiles/', views.search_mobiles, name='search_mobiles'),
]