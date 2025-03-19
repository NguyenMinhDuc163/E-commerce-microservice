from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/user_service/login/', include('user_login.urls')),
    path('api/user_service/user/', include('user_model.urls')),
    path('api/user_service/', include('user_info.urls')),
]
