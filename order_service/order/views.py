from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import OrderItem
from .serializers import OrderItemSerializer, UpdateOrderItemSerializer
import requests
import json
from django.utils.timezone import now
from django.views.decorators.csrf import csrf_exempt
from rest_framework.generics import RetrieveAPIView
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes


# Hàm gọi API verify_token để lấy user_id
def verify_token(token):
    url = 'http://127.0.0.1:8002/api/user_service/verify_token/'
    headers = {'Authorization': f'Bearer {token}'}
    print(token)
    response = requests.post(url, headers=headers)
    print(response)
    if response.status_code == 200:
        return response.json().get('user_id')
    return None

# Hàm gọi API product_service để lấy thông tin sản phẩm
def get_product(product_id, type):
    if type == "book":
        url = f'http://localhost:8001/api/product_service/book/get_book/{product_id}/'
        response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None

# Hàm gọi API shipment_service để tạo shipment mới
def create_shipment(user_id, order_item_id, username, address, phone, shipment_type):
    url = 'http://127.0.0.1:8006/api/shipment_service/create/'
    data = {
        'user_id': user_id,
        'order_item_id': order_item_id,
        'username': username,
        'address': address,
        'phone': phone,
        'shipment_type': shipment_type
    }
    response = requests.post(url, json=data)
    if response.status_code == 200:
        return response.json().get('shipment_id')
    return None


# Hàm gọi API payment_service để tạo payment mới
def create_payment(order_item_id, user_id, payment_type):
    url = 'http://127.0.0.1:8007/api/payment_service/create/'
    data = {
        'order_item_id': order_item_id,
        'user_id': user_id,
        'payment_type': payment_type,
    }
    response = requests.post(url, json=data)
    if response.status_code == 200:
        return response.json().get('payment_id')
    return None

class AddToOrderView(APIView):
    @extend_schema(
        summary="Thêm sản phẩm vào đơn hàng",
        description="API để thêm sản phẩm vào đơn hàng mới",
        request={
            'application/json': {
                'type': 'object',
                'properties': {
                    'product_id': {'type': 'string'},
                    'quantity': {'type': 'integer'},
                    'type': {'type': 'string', 'enum': ['book', 'mobile', 'clothes']},
                    'username': {'type': 'string'},
                    'address': {'type': 'string'},
                    'phone': {'type': 'string'},
                    'shipment_type': {'type': 'string'},
                    'payment_type': {'type': 'string'}
                },
                'required': ['product_id', 'quantity', 'type', 'username', 'address', 'phone', 'shipment_type', 'payment_type']
            }
        },
        responses={201: OrderItemSerializer}
    )
    @csrf_exempt
    def post(self, request):
        token = request.headers.get('Authorization').split()[1]
        user_id = verify_token(token)

        if not user_id:
            return Response({'error': 'Invalid token.'}, status=status.HTTP_401_UNAUTHORIZED)

        data = request.data
        product_id = data.get('product_id')
        quantity = data.get('quantity')
        type = data.get('type')
        product = get_product(product_id, type)

        if not product:
            return Response({'error': 'Invalid product ID.'}, status=status.HTTP_400_BAD_REQUEST)

        total_price = quantity * product.get('price', 0)

        order_item = OrderItem.objects.create(
            user_id=user_id,
            product_id=product_id,
            type=product.get('type'),
            quantity=quantity,
            created_at=now().date().isoformat(),
            updated_at=now().date().isoformat(),
            payment_id=None,
            shipment_id=None,
            total=total_price
        )

        shipment_id = create_shipment(
            user_id=user_id,
            order_item_id=order_item.order_item_id,
            username=data.get('username'),
            address=data.get('address'),
            phone=data.get('phone'),
            shipment_type=data.get('shipment_type')
        )

        if not shipment_id:
            return Response({'error': 'Shipment creation failed.'}, status=status.HTTP_400_BAD_REQUEST)

        order_item.shipment_id = shipment_id
        order_item.save()

        payment_id = create_payment(
            order_item_id=order_item.order_item_id,
            user_id=user_id,
            payment_type=data.get('payment_type')
        )

        if not payment_id:
            return Response({'error': 'Payment creation failed.'}, status=status.HTTP_400_BAD_REQUEST)

        order_item.payment_id = payment_id
        order_item.save()

        serializer = OrderItemSerializer(order_item)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class OrderItemListView(APIView):
    @extend_schema(
        summary="Lấy danh sách tất cả đơn hàng",
        description="API để lấy danh sách tất cả các đơn hàng",
        responses={200: OrderItemSerializer(many=True)}
    )
    def get(self, request):
        order_items = OrderItem.objects.all()
        serializer = OrderItemSerializer(order_items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class OrderListByStatus(APIView):
    @extend_schema(
        summary="Lấy danh sách đơn hàng theo trạng thái",
        description="API để lấy danh sách các đơn hàng theo trạng thái",
        parameters=[
            OpenApiParameter(
                name='status',
                type=OpenApiTypes.STR,
                description='Trạng thái đơn hàng'
            )
        ],
        responses={200: OrderItemSerializer(many=True)}
    )
    def get(self, request):
        status_param = request.query_params.get('status')
        order_items = OrderItem.objects.filter(status=status_param)
        serializer = OrderItemSerializer(order_items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# class OrderItemView(APIView):
#     def get(self, request):
#         token = request.headers.get('Authorization', '').split('Bearer ')[-1]
#         user_id = verify_token(token)
#
#         if not user_id:
#             return Response({'error': 'Invalid token.'}, status=status.HTTP_401_UNAUTHORIZED)
#
#         order_id = request.query_params.get('order_id')
#         created_at = request.query_params.get('created_at')
#         order_item = OrderItem.objects.filter(user_id=user_id, order_item_id=order_id, created_at=created_at).first()
#
#         if not order_item:
#             return Response({'error': 'Order item not found.'}, status=status.HTTP_404_NOT_FOUND)
#
#         order_total = 0
#         product = self.get_product(order_item.type, order_item.product_id)
#         shipment = self.get_shipment(order_item.shipment_id)
#
#         if product:
#             order_total = order_item.quantity * product.get('price', 0) * (100 - product.get('sale', 0)) / 100
#
#         if shipment:
#             order_total += shipment.get('price', 0)
#
#         response_data = {
#             'order_item': OrderItemSerializer(order_item).data,
#             'total': order_total
#         }
#         return Response(response_data, status=status.HTTP_200_OK)
#
#     def get_product(self, type, product_id):
#         if type == 'book':
#             product_url = f"http://localhost:4002/api/book/detail/{product_id}/"
#         elif type == 'mobile':
#             product_url = f"http://localhost:4002/api/mobile/detail/{product_id}/"
#         elif type == 'clothes':
#             product_url = f"http://localhost:4002/api/clothes/detail/{product_id}/"
#         else:
#             return None
#
#         response = requests.get(product_url)
#         if response.status_code == 200:
#             return response.json()
#         return None
#
#     def get_shipment(self, shipment_id):
#         shipment_url = f"http://localhost:4002/api/shipment/detail/{shipment_id}/"
#         response = requests.get(shipment_url)
#         if response.status_code == 200:
#             return response.json()
#         return None

class OrderDetailView(RetrieveAPIView):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    lookup_field = 'order_item_id'

    @extend_schema(
        summary="Lấy chi tiết đơn hàng",
        description="API để lấy thông tin chi tiết của một đơn hàng",
        parameters=[
            OpenApiParameter(
                name='order_item_id',
                type=OpenApiTypes.INT,
                description='ID của đơn hàng'
            )
        ],
        responses={200: OrderItemSerializer}
    )
    def get(self, request, *args, **kwargs):
        # token = request.headers.get('Authorization').split()[1]
        # user_id = verify_token(token)
        # if not user_id:
        #     return Response({'status': 'Failed', 'status_code': 401, 'message': 'Invalid token'},
        #                     status=status.HTTP_401_UNAUTHORIZED)
        return super().get(request, *args, **kwargs)
