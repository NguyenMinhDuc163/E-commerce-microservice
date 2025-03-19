from django.contrib import admin
from .models import Brand, Clothes

admin.site.register([Brand, Clothes])
