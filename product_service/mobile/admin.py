from django.contrib import admin
from .models import Producer, Mobile

admin.site.register([Producer, Mobile])
