from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny  # Thêm dòng này
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes

from user_model.serializers import UserSerializer


# Create your views here.

class CreateUserView(APIView):
    permission_classes = [AllowAny]  # Thêm dòng này

    @extend_schema(
        summary="Tạo tài khoản người dùng mới",
        description="API để tạo một tài khoản người dùng mới",
        request=UserSerializer,
        responses={
            201: UserSerializer,
            400: {
                'type': 'object',
                'properties': {
                    'field_name': {'type': 'array', 'items': {'type': 'string'}}
                }
            }
        }
    )
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            user = serializer.data
            user['account']['password'] = ''
            return JsonResponse(user, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)