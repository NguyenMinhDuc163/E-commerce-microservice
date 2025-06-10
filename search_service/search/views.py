from rest_framework.decorators import api_view
from rest_framework.response import Response
import requests
from search_service.settings import PRODUCT_SERVICE_BOOK_URL, PRODUCT_SERVICE_CLOTHES_URL, PRODUCT_SERVICE_MOBILE_URL
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes
import logging

logger = logging.getLogger(__name__)

# Định nghĩa schema cho response
BOOK_RESPONSE_SCHEMA = {
    'type': 'array',
    'items': {
        'type': 'object',
        'properties': {
            'id': {'type': 'string', 'description': 'ID của sách'},
            'title': {'type': 'string', 'description': 'Tiêu đề sách'},
            'author': {'type': 'string', 'description': 'Tác giả'},
            'publisher': {'type': 'string', 'description': 'Nhà xuất bản'},
            'price': {'type': 'number', 'description': 'Giá sách'},
            'description': {'type': 'string', 'description': 'Mô tả sách'},
            'image': {'type': 'string', 'description': 'URL ảnh bìa sách'}
        }
    }
}

MOBILE_RESPONSE_SCHEMA = {
    'type': 'array',
    'items': {
        'type': 'object',
        'properties': {
            'id': {'type': 'string', 'description': 'ID của điện thoại'},
            'name': {'type': 'string', 'description': 'Tên điện thoại'},
            'brand': {'type': 'string', 'description': 'Thương hiệu'},
            'price': {'type': 'number', 'description': 'Giá điện thoại'},
            'description': {'type': 'string', 'description': 'Mô tả điện thoại'},
            'image': {'type': 'string', 'description': 'URL ảnh điện thoại'}
        }
    }
}

CLOTHES_RESPONSE_SCHEMA = {
    'type': 'array',
    'items': {
        'type': 'object',
        'properties': {
            'id': {'type': 'string', 'description': 'ID của sản phẩm'},
            'name': {'type': 'string', 'description': 'Tên sản phẩm'},
            'brand': {'type': 'string', 'description': 'Thương hiệu'},
            'price': {'type': 'number', 'description': 'Giá sản phẩm'},
            'description': {'type': 'string', 'description': 'Mô tả sản phẩm'},
            'image': {'type': 'string', 'description': 'URL ảnh sản phẩm'}
        }
    }
}

@extend_schema(
    summary="Tìm kiếm tất cả sản phẩm",
    description="API để tìm kiếm sản phẩm trên tất cả các loại (sách, điện thoại, quần áo)",
    parameters=[
        OpenApiParameter(
            name='key',
            type=OpenApiTypes.STR,
            description='Từ khóa tìm kiếm'
        )
    ],
    responses={
        200: {
            'type': 'array',
            'items': {
                'oneOf': [
                    {'$ref': '#/components/schemas/BookResponse'},
                    {'$ref': '#/components/schemas/MobileResponse'},
                    {'$ref': '#/components/schemas/ClothesResponse'}
                ]
            }
        }
    }
)
@api_view(['GET'])
def search_all(request):
    key = request.query_params.get('key', '')
    result = []
    
    # Search books with error handling
    try:
        book_response = requests.get(
            PRODUCT_SERVICE_BOOK_URL + f'/search_books?key={key}',
            timeout=10
        )
        if book_response.status_code == 200:
            result += book_response.json()
    except Exception as e:
        logger.error(f"Error calling book service: {e}")
    
    # Search clothes with error handling
    try:
        clothes_response = requests.get(
            PRODUCT_SERVICE_CLOTHES_URL + f'/search_clothes?key={key}',
            timeout=10
        )
        if clothes_response.status_code == 200:
            result += clothes_response.json()
    except Exception as e:
        logger.error(f"Error calling clothes service: {e}")
    
    # Search mobiles with error handling
    try:
        mobile_response = requests.get(
            PRODUCT_SERVICE_MOBILE_URL + f'/search_mobiles?key={key}',
            timeout=10
        )
        if mobile_response.status_code == 200:
            result += mobile_response.json()
    except Exception as e:
        logger.error(f"Error calling mobile service: {e}")
    
    return Response(result)


@extend_schema(
    summary="Tìm kiếm sách",
    description="API để tìm kiếm sách theo từ khóa",
    parameters=[
        OpenApiParameter(
            name='key',
            type=OpenApiTypes.STR,
            description='Từ khóa tìm kiếm'
        )
    ],
    responses={200: BOOK_RESPONSE_SCHEMA}
)
@api_view(['GET'])
def search_books(request):
    key = request.query_params.get('key', '')
    try:
        response = requests.get(
            PRODUCT_SERVICE_BOOK_URL + f'/search_books?key={key}',
            timeout=10
        )
        if response.status_code == 200:
            return Response(response.json())
        else:
            return Response({'error': f'Product service returned status {response.status_code}'}, status=500)
    except requests.exceptions.Timeout:
        return Response({'error': 'Request timeout when calling product service'}, status=504)
    except requests.exceptions.ConnectionError:
        return Response({'error': 'Connection error when calling product service'}, status=503)
    except Exception as e:
        logger.error(f"Error calling book service: {e}")
        return Response({'error': 'Internal server error'}, status=500)


@extend_schema(
    summary="Tìm kiếm quần áo",
    description="API để tìm kiếm quần áo theo từ khóa",
    parameters=[
        OpenApiParameter(
            name='key',
            type=OpenApiTypes.STR,
            description='Từ khóa tìm kiếm'
        )
    ],
    responses={200: CLOTHES_RESPONSE_SCHEMA}
)
@api_view(['GET'])
def search_clothes(request):
    key = request.query_params.get('key', '')
    try:
        response = requests.get(
            PRODUCT_SERVICE_CLOTHES_URL + f'/search_clothes?key={key}',
            timeout=10
        )
        if response.status_code == 200:
            return Response(response.json())
        else:
            return Response({'error': f'Product service returned status {response.status_code}'}, status=500)
    except requests.exceptions.Timeout:
        return Response({'error': 'Request timeout when calling product service'}, status=504)
    except requests.exceptions.ConnectionError:
        return Response({'error': 'Connection error when calling product service'}, status=503)
    except Exception as e:
        logger.error(f"Error calling clothes service: {e}")
        return Response({'error': 'Internal server error'}, status=500)


@extend_schema(
    summary="Tìm kiếm điện thoại",
    description="API để tìm kiếm điện thoại theo từ khóa",
    parameters=[
        OpenApiParameter(
            name='key',
            type=OpenApiTypes.STR,
            description='Từ khóa tìm kiếm'
        )
    ],
    responses={200: MOBILE_RESPONSE_SCHEMA}
)
@api_view(['GET'])
def search_mobiles(request):
    key = request.query_params.get('key', '')
    try:
        response = requests.get(
            PRODUCT_SERVICE_MOBILE_URL + f'/search_mobiles?key={key}',
            timeout=10
        )
        if response.status_code == 200:
            return Response(response.json())
        else:
            return Response({'error': f'Product service returned status {response.status_code}'}, status=500)
    except requests.exceptions.Timeout:
        return Response({'error': 'Request timeout when calling product service'}, status=504)
    except requests.exceptions.ConnectionError:
        return Response({'error': 'Connection error when calling product service'}, status=503)
    except Exception as e:
        logger.error(f"Error calling mobile service: {e}")
        return Response({'error': 'Internal server error'}, status=500)
