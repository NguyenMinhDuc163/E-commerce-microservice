from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes

from user_model.models import User
from user_model.serializers import UserSerializer
from .authentication import SafeJWTAuthentication

# Create your views here.

class VerifyTokenView(APIView):
    authentication_classes = [SafeJWTAuthentication]
    
    @extend_schema(
        summary="Xác thực token",
        description="API để xác thực token JWT của người dùng",
        responses={
            200: {
                'type': 'object',
                'properties': {
                    'user_id': {'type': 'integer', 'description': 'ID của người dùng'},
                    'message': {'type': 'string', 'description': 'Thông báo xác thực thành công'}
                }
            },
            401: {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string', 'description': 'Thông báo token không hợp lệ'}
                }
            }
        }
    )
    def post(self, request):
        if request.user:
            account = request.user
            user = User.objects.get(account__username=account.username)
            return JsonResponse({"user_id": user.id, "message": "Token is valid"}, status=status.HTTP_200_OK)

        return JsonResponse({'message': 'Token is invalid'}, status=status.HTTP_401_UNAUTHORIZED)

class UserInfoView(APIView):
    authentication_classes = [SafeJWTAuthentication]
    
    @extend_schema(
        summary="Lấy thông tin người dùng",
        description="API để lấy thông tin chi tiết của người dùng đang đăng nhập",
        responses={
            200: {
                'type': 'object',
                'properties': {
                    'id': {'type': 'integer', 'description': 'ID của người dùng'},
                    'username': {'type': 'string', 'description': 'Tên đăng nhập'},
                    'email': {'type': 'string', 'description': 'Email'},
                    'first_name': {'type': 'string', 'description': 'Tên'},
                    'last_name': {'type': 'string', 'description': 'Họ'},
                    'full_name': {'type': 'string', 'description': 'Họ và tên đầy đủ'},
                    'phone': {'type': 'string', 'description': 'Số điện thoại'},
                    'address': {'type': 'string', 'description': 'Địa chỉ'}
                }
            },
            401: {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string', 'description': 'Thông báo không có quyền truy cập'}
                }
            }
        }
    )
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