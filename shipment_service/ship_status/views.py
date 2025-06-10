from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from .models import Shipment
from .serializers import ShipmentSerializer
import requests
import json
from rest_framework.generics import RetrieveAPIView
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes


def verify_token(token):
    try:
        url = 'http://user-service-container:8000/api/user_service/verify_token/'
        headers = {'Authorization': f'Bearer {token}'}
        response = requests.post(url, headers=headers, timeout=10)
        print(f"User service response status: {response.status_code}")
        print(f"User service response text: {response.text[:200]}...")  # First 200 chars
        
        if response.status_code == 200:
            try:
                return response.json().get('user_id')
            except ValueError as e:
                print(f"JSON decode error from user service: {e}")
                print(f"Response content: {response.text}")
                return None
        else:
            print(f"User service returned status {response.status_code}: {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Request to user service failed: {e}")
        return None


def check_order_item(order_item_id):
    try:
        url = f'http://order-service-container:8000/api/order_service/detail/{order_item_id}/'
        response = requests.get(url, timeout=10)
        print(f"Order service response status: {response.status_code}")
        print(f"Order service response text: {response.text[:200]}...")  # First 200 chars
        
        if response.status_code == 200:
            try:
                return response.json()
            except ValueError as e:
                print(f"JSON decode error from order service: {e}")
                print(f"Response content: {response.text}")
                return None
        else:
            print(f"Order service returned status {response.status_code}: {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Request to order service failed: {e}")
        return None

class ShipmentCreateView(APIView):
    @extend_schema(
        summary="Tạo đơn vận chuyển mới",
        description="API để tạo một đơn vận chuyển mới cho một đơn hàng",
        request={
            'application/json': {
                'type': 'object',
                'properties': {
                    'order_item_id': {'type': 'integer', 'description': 'ID của đơn hàng'},
                },
                'required': ['order_item_id']
            }
        },
        responses={
            200: {
                'type': 'object',
                'properties': {
                    'shipment_id': {'type': 'integer', 'description': 'ID của đơn vận chuyển mới tạo'}
                }
            },
            400: {
                'type': 'object',
                'properties': {
                    'status': {'type': 'string'},
                    'status_code': {'type': 'integer'},
                    'message': {'type': 'string'}
                }
            },
            401: {
                'type': 'object',
                'properties': {
                    'status': {'type': 'string'},
                    'status_code': {'type': 'integer'},
                    'message': {'type': 'string'}
                }
            }
        }
    )
    def post(self, request):
        # Lấy token từ header Authorization
        authorization_header = request.headers.get('Authorization')
        if not authorization_header:
            return Response({'status': 'Failed', 'status_code': 401, 'message': 'Missing Authorization header'},
                            status=status.HTTP_401_UNAUTHORIZED)

        try:
            # Tách token từ header (bỏ phần 'Bearer ')
            token = authorization_header.split()[1]

            # Xác thực token và lấy user_id
            user_id = verify_token(token)
            print("======= > ", user_id)

            if not user_id:
                return Response({'status': 'Failed', 'status_code': 401, 'message': 'Invalid token'},
                                status=status.HTTP_401_UNAUTHORIZED)

            # Lấy thông tin chi tiết của user dùng token
            user_info_url = 'http://user-service-container:8000/api/user_service/user_info/'
            user_info_headers = {'Authorization': f'Bearer {token}', 'Accept': 'application/json'}
            user_info_response = requests.get(user_info_url, headers=user_info_headers, timeout=10)

            print(f"User info response status: {user_info_response.status_code}")
            print(f"User info response text: {user_info_response.text[:200]}...")

            if user_info_response.status_code != 200:
                return Response({'status': 'Failed', 'status_code': 400, 
                               'message': f'Cannot get user information. Status: {user_info_response.status_code}, Response: {user_info_response.text[:100]}'},
                                status=status.HTTP_400_BAD_REQUEST)

            try:
                user_info = user_info_response.json()
            except ValueError as e:
                return Response({'status': 'Failed', 'status_code': 400, 
                               'message': f'Invalid JSON response from user service: {e}. Response: {user_info_response.text[:100]}'},
                                status=status.HTTP_400_BAD_REQUEST)

            # Xử lý dữ liệu từ request
            if request.content_type == 'application/json':
                data = request.data
                order_item_id = data.get('order_item_id')
                if not check_order_item(order_item_id):
                    return Response({'status': 'Failed', 'status_code': 400, 'message': 'Invalid order item ID'},
                                    status=status.HTTP_400_BAD_REQUEST)

                # Tạo dữ liệu cho serializer
                shipment_data = {
                    'user_id': user_id,
                    'order_item_id': order_item_id,
                    'username': user_info.get('username'),
                    'address': user_info.get('address'),
                    'phone': user_info.get('phone'),
                    'shipment_status': 'Not ship',
                    'shipment_type': data.get('shipment_type', 'ECONOMICAL')  # Lấy từ request hoặc dùng mặc định
                }

                serializer = ShipmentSerializer(data=shipment_data)
                print(serializer)
                if serializer.is_valid():
                    shipment = serializer.save()
                    return Response({'shipment_id': shipment.id}, status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            return Response({'status': 'Failed', 'status_code': 400, 'message': 'Invalid content type.'},
                            status=status.HTTP_400_BAD_REQUEST)
        except IndexError:
            return Response({'status': 'Failed', 'status_code': 401, 'message': 'Invalid Authorization format'},
                            status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({'status': 'Failed', 'status_code': 500, 'message': str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ShipmentStatusView(APIView):
    @extend_schema(
        summary="Xem trạng thái vận chuyển",
        description="API để xem trạng thái vận chuyển của một đơn hàng",
        responses={
            200: {
                'type': 'object',
                'properties': {
                    'status': {'type': 'string'},
                    'status_code': {'type': 'integer'},
                    'message': {'type': 'object'}
                }
            },
            400: {
                'type': 'object',
                'properties': {
                    'status': {'type': 'string'},
                    'status_code': {'type': 'integer'},
                    'message': {'type': 'string'}
                }
            }
        }
    )
    def post(self, request):
        #         if request.content_type == 'application/json':
        #             data = json.loads(request.body)
        #             username = data.get("username")
        #             shipment_data = Shipment.objects.filter(username=username).values().first()
        #             if shipment_data:
        #                 return Response({'status': 'Success', 'status_code': 200, 'message': shipment_data},
        #                                 status=status.HTTP_200_OK)
        #             return Response({'status': 'Failed', 'status_code': 400, 'message': 'User data is not available.'},
        #                             status=status.HTTP_400_BAD_REQUEST)
        return Response({'status': 'Failed', 'status_code': 400, 'message': 'Invalid content type.'},
                        status=status.HTTP_400_BAD_REQUEST)


class ShipmentDetailView(RetrieveAPIView):
    queryset = Shipment.objects.all()
    serializer_class = ShipmentSerializer
    lookup_field = 'id'

    @extend_schema(
        summary="Xem chi tiết đơn vận chuyển",
        description="API để xem chi tiết của một đơn vận chuyển theo ID",
        parameters=[
            OpenApiParameter(
                name='id',
                type=OpenApiTypes.INT,
                location=OpenApiParameter.PATH,
                description='ID của đơn vận chuyển'
            )
        ],
        responses={
            200: ShipmentSerializer,
            404: {
                'type': 'object',
                'properties': {
                    'detail': {'type': 'string'}
                }
            }
        }
    )
    def get(self, request, *args, **kwargs):
        # token = request.headers.get('Authorization').split()[1]
        # user_id = verify_token(token)
        # if not user_id:
        #     return Response({'status': 'Failed', 'status_code': 401, 'message': 'Invalid token'},
        #                     status=status.HTTP_401_UNAUTHORIZED)
        return super().get(request, *args, **kwargs)
