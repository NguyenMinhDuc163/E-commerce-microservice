from django.contrib.auth.hashers import check_password
from django.http import JsonResponse
from rest_framework import status
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes

from .utils import generate_access_token, generate_refresh_token
from user_model.models import Account


class LoginAPIView(APIView):
    @extend_schema(
        summary="Đăng nhập người dùng",
        description="API để đăng nhập và lấy token JWT",
        request={
            'application/json': {
                'type': 'object',
                'properties': {
                    'username': {'type': 'string', 'description': 'Tên đăng nhập'},
                    'password': {'type': 'string', 'description': 'Mật khẩu'}
                },
                'required': ['username', 'password']
            }
        },
        responses={
            200: {
                'type': 'object',
                'properties': {
                    'token': {'type': 'string', 'description': 'Access token JWT'},
                    'refresh': {'type': 'string', 'description': 'Refresh token JWT'}
                }
            },
            401: {
                'type': 'object',
                'properties': {
                    'error': {'type': 'string', 'description': 'Thông báo lỗi xác thực'}
                }
            }
        }
    )
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        # Xác thực thông tin đăng nhập
        try:
            account = Account.objects.get(username=username)
            if check_password(password, account.password):
                access_token = generate_access_token(account.username)
                refresh_token = generate_refresh_token(account.username)

                return JsonResponse({
                    'token': str(access_token),
                    'refresh': str(refresh_token)
                }, status=status.HTTP_200_OK)
        except Account.DoesNotExist:
            return JsonResponse({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
