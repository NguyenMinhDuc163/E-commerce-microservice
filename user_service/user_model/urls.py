from django.urls import path

from user_model.views import CreateUserView

urlpatterns = [
    path('create_user/', CreateUserView.as_view(), name='create_user'),

]