from django.http import JsonResponse
from rest_framework import status
from rest_framework.views import APIView
import requests
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

from cart.authentication import SafeJWTAuthentication
from cart.models import CartItem
from cart.serializers import CartItemSerializer


# Create your views here.
def verify(request):
    try:
        # Try same URL as order_service which works
        url_verify = 'http://user-service-container:8000/api/user_service/verify_token/'
        
        # Alternative: Try using container IP - let's debug first
        print(f"DEBUG: About to call URL: {url_verify}")
        
        # Check if Authorization header exists
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            print("ERROR: No Authorization header found")
            return {'status': False, 'error': 'No Authorization header'}
        
        # Extract token
        try:
            token = auth_header.split()[1]
        except IndexError:
            print("ERROR: Invalid Authorization header format")
            return {'status': False, 'error': 'Invalid Authorization header format'}

        headers = {
            'Authorization': f'Bearer {token}'
        }

        print(f"DEBUG: Calling user_service at {url_verify}")
        print(f"DEBUG: Token: {token[:20]}...")
        
        response_verify = requests.post(url_verify, headers=headers, timeout=10)
        
        print(f"DEBUG: User service response status: {response_verify.status_code}")
        print(f"DEBUG: User service response headers: {dict(response_verify.headers)}")
        print(f"DEBUG: User service response: {response_verify.text[:500]}...")  # Only first 500 chars
        
        # If we get HTML error, it means Django is rejecting the request
        if response_verify.status_code == 400 and 'html' in response_verify.text.lower():
            print("ERROR: User service is returning HTML error page - likely ALLOWED_HOSTS issue")
            print("DEBUG: Let's try a different approach...")
        
        if response_verify.status_code == 200:
            response_data = response_verify.json()
            return {
                'user_id': response_data['user_id'],
                'status': True
            }
        else:
            return {
                'status': False,
                'error': f'User service returned {response_verify.status_code}'
            }
            
    except requests.exceptions.RequestException as e:
        print(f"ERROR: Request to user service failed: {e}")
        return {'status': False, 'error': f'Request failed: {e}'}
    except Exception as e:
        print(f"ERROR: Unexpected error in verify: {e}")
        return {'status': False, 'error': f'Unexpected error: {e}'}

class CartView(APIView):

    authentication_classes = [SafeJWTAuthentication]

    @extend_schema(
        summary='Lấy danh sách giỏ hàng',
        description='API này trả về danh sách các sản phẩm trong giỏ hàng của người dùng',
        responses={
            200: CartItemSerializer(many=True),
            401: OpenApiTypes.OBJECT
        },
        parameters=[
            OpenApiParameter(
                name='Authorization',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.HEADER,
                description='Bearer token để xác thực người dùng'
            )
        ]
    )
    def get(self, request):
        data_verify = verify(request)
        if not data_verify['status']:
            return JsonResponse({'message': 'Token is invalid'}, status=status.HTTP_401_UNAUTHORIZED)

        user_id = data_verify['user_id']
        cart_list = CartItem.objects.filter(user_id=user_id)

        cart = []
        for item in cart_list:
            cait_item = CartItemSerializer(item).data
            cart.append(cait_item)

        return JsonResponse({"data": cart}, status=status.HTTP_200_OK, safe=False)


    @extend_schema(
        summary='Thêm sản phẩm vào giỏ hàng',
        description='API này cho phép thêm một sản phẩm mới vào giỏ hàng',
        request=CartItemSerializer,
        responses={
            201: CartItemSerializer,
            400: OpenApiTypes.OBJECT,
            401: OpenApiTypes.OBJECT
        },
        parameters=[
            OpenApiParameter(
                name='Authorization',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.HEADER,
                description='Bearer token để xác thực người dùng'
            )
        ]
    )
    def post(self, request):
        data_verify = verify(request)
        if not data_verify['status']:
            return JsonResponse({'message': 'Token is invalid'}, status=status.HTTP_401_UNAUTHORIZED)

        user_id = data_verify['user_id']
        data = request.data
        data['user_id'] = user_id
        serializer = CartItemSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        summary='Xóa sản phẩm khỏi giỏ hàng',
        description='API này cho phép xóa một sản phẩm khỏi giỏ hàng',
        responses={
            200: OpenApiTypes.OBJECT,
            401: OpenApiTypes.OBJECT,
            404: OpenApiTypes.OBJECT
        },
        parameters=[
            OpenApiParameter(
                name='Authorization',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.HEADER,
                description='Bearer token để xác thực người dùng'
            ),
            OpenApiParameter(
                name='cart_id',
                type=OpenApiTypes.INT,
                location=OpenApiParameter.PATH,
                description='ID của sản phẩm trong giỏ hàng cần xóa'
            )
        ]
    )
    def delete(self, request, cart_id):
        data_verify = verify(request)
        if not data_verify['status']:
            return JsonResponse({'message': 'Token is invalid'}, status=status.HTTP_401_UNAUTHORIZED)

        user_id = data_verify['user_id']

        cart_item = CartItem.objects.filter(user_id=user_id, id=cart_id).first()
        if cart_item:
            cart_item.delete()
            return JsonResponse({'message': 'Delete success'}, status=status.HTTP_200_OK)
        return JsonResponse({'message': 'Cart item not found'}, status=status.HTTP_404_NOT_FOUND)










