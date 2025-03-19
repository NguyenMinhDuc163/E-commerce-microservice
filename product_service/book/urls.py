from django.urls import path
from . import views

urlpatterns = [
    path('get_books/', views.get_books, name='get_books'),
    path('get_book/<str:pk>/', views.get_book, name='get_book'),
    path('search_books/', views.search_books, name='search_books'),
]