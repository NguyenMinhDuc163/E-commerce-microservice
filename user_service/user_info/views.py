from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView

from user_model.models import User
from user_model.serializers import UserSerializer
from .authentication import SafeJWTAuthentication

# Create your views here.

class VerifyTokenView(APIView):
    authentication_classes = [SafeJWTAuthentication]
    def post(self, request):
        if request.user:
            account = request.user
            user = User.objects.get(account__username=account.username)
            return JsonResponse({"user_id": user.id, "message": "Token is valid"}, status=status.HTTP_200_OK)

        return JsonResponse({'message': 'Token is invalid'}, status=status.HTTP_401_UNAUTHORIZED)

class UserInfoView(APIView):
    authentication_classes = [SafeJWTAuthentication]
    def get(self, request):
        print(request)
        account = request.user
        serializer = UserSerializer(User.objects.get(account__username=account.username))

        user = {
            'id': serializer.data['id'],
            'username': serializer.data['account']['username'],
            'email': serializer.data['email'],
            'first_name': serializer.data['fullname']['first_name'],
            'last_name': serializer.data['fullname']['last_name'],
            'full_name': serializer.data['fullname']['first_name'] + ' ' + serializer.data['fullname']['last_name'],
            'phone': serializer.data['phone'],
            'address': serializer.data['address']['address']
        }
        return JsonResponse(user, status=status.HTTP_200_OK)