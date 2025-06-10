from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from .models import PaymentStatus
from .serializers import PaymentStatusSerializer
from shipment_update.views import shipment_details_update
import requests
from django.utils.timezone import now
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes

def verify_token(token):
    try:
        url = 'http://user-service-container:8000/api/user_service/verify_token/'
        headers = {'Authorization': f'Bearer {token}'}
        print(f"Calling user service with token: {token[:20]}...")
        response = requests.post(url, headers=headers, timeout=10)
        print(f"User service response status: {response.status_code}")
        print(f"User service response: {response.text[:200]}...")
        
        if response.status_code == 200:
            try:
                return response.json().get('user_id')
            except ValueError as e:
                print(f"JSON decode error from user service: {e}")
                return None
        return None
    except requests.exceptions.RequestException as e:
        print(f"Request to user service failed: {e}")
        return None

#Hàm kiểm tra order_item_id
def check_order_item(order_item_id):
    try:
        url = f'http://order-service-container:8000/api/order_service/detail/{order_item_id}/'
        response = requests.get(url, timeout=10)
        print(f"Order service response status: {response.status_code}")
        print(f"Order service response: {response.text[:200]}...")
        
        if response.status_code == 200:
            try:
                return response.json()
            except ValueError as e:
                print(f"JSON decode error from order service: {e}")
                return None
        return None
    except requests.exceptions.RequestException as e:
        print(f"Request to order service failed: {e}")
        return None


def check_shipment(shipment_id):
    try:
        url = f'http://shipment-service-container:8000/api/shipment_service/detail/{shipment_id}/'
        response = requests.get(url, timeout=10)
        print(f"Shipment service response status: {response.status_code}")
        print(f"Shipment service response: {response.text[:200]}...")
        
        if response.status_code == 200:
            try:
                return response.json()
            except ValueError as e:
                print(f"JSON decode error from shipment service: {e}")
                return None
        return None
    except requests.exceptions.RequestException as e:
        print(f"Request to shipment service failed: {e}")
        return None

class CreatePaymentView(APIView):
    @extend_schema(
        summary="Tạo thanh toán mới",
        description="API để tạo một thanh toán mới cho đơn hàng",
        request={
            'application/json': {
                'type': 'object',
                'properties': {
                    'order_item_id': {'type': 'integer', 'description': 'ID của đơn hàng'},
                    'payment_type': {'type': 'string', 'description': 'Loại thanh toán'},
                },
                'required': ['order_item_id', 'payment_type']
            }
        },
        responses={
            200: {
                'type': 'object',
                'properties': {
                    'payment_id': {'type': 'integer', 'description': 'ID của thanh toán mới tạo'}
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
    @csrf_exempt
    def post(self, request):
        # Lấy token từ header
        authorization_header = request.headers.get('Authorization')
        if not authorization_header:
            return Response({'status': 'Failed', 'status_code': 401, 'message': 'Missing Authorization header'},
                            status=status.HTTP_401_UNAUTHORIZED)

        try:
            # Tách token từ header
            token = authorization_header.split()[1]

            # Xác thực token và lấy user_id
            user_id = verify_token(token)
            print("=====>", user_id)

            if not user_id:
                return Response({'status': 'Failed', 'status_code': 401, 'message': 'Invalid token'},
                                status=status.HTTP_401_UNAUTHORIZED)

            data = request.data
            order_item_id = data.get('order_item_id')
            order_item = check_order_item(order_item_id)
            print(order_item)
            if not order_item:
                return Response({'status': 'Failed', 'status_code': 400, 'message': 'Invalid order item ID.'},
                                status=status.HTTP_400_BAD_REQUEST)

            # Tạo một bản sao của data để không thay đổi dữ liệu gốc
            data_copy = data.copy() if hasattr(data, 'copy') else dict(data)
            data_copy['user_id'] = user_id
            data_copy['order_item_id'] = order_item_id
            data_copy['status'] = 'Success'
            data_copy['payment_date'] = now().date().isoformat()

            shipment = check_shipment(order_item.get('shipment_id'))
            if not shipment:
                return Response({'status': 'Failed', 'status_code': 400, 'message': 'Invalid shipment ID.'},
                                status=status.HTTP_400_BAD_REQUEST)

            data_copy['price'] = shipment.get('price') + order_item.get('total')
            serializer = PaymentStatusSerializer(data=data_copy)
            print("Data to be stored:", data_copy)

            if serializer.is_valid():
                payment = serializer.save()
                print("Data stored successfully")
                return Response({'payment_id': payment.id}, status=status.HTTP_200_OK)
            else:
                print("Errors:", serializer.errors)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except IndexError:
            return Response({'status': 'Failed', 'status_code': 401, 'message': 'Invalid Authorization format'},
                            status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({'status': 'Failed', 'status_code': 500, 'message': str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


