from django.urls import path
from . import views

urlpatterns = [
    path('search_by_key/', views.search_all, name='search_by_key'),
    path('search_books/', views.search_books, name='search_books'),
    path('search_clothes/', views.search_clothes, name='search_clothes'),
    path('search_mobiles/', views.search_mobiles, name='search_mobiles'),
]