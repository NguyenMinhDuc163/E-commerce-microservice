from django.contrib import admin
from .models import Book, Author, Publisher, Category

admin.site.register([Book, Author, Publisher, Category])

