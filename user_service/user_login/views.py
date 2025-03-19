from django.contrib.auth.hashers import check_password
from django.http import JsonResponse
from rest_framework import status
from rest_framework.views import APIView

from .utils import generate_access_token, generate_refresh_token
from user_model.models import Account


class LoginAPIView(APIView):
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
