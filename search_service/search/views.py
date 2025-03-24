from rest_framework.decorators import api_view
from rest_framework.response import Response
import requests
from search_service.settings import PRODUCT_SERVICE_BOOK_URL, PRODUCT_SERVICE_CLOTHES_URL, PRODUCT_SERVICE_MOBILE_URL
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes

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
    book_response = requests.get(PRODUCT_SERVICE_BOOK_URL + f'/search_books?key={key}')
    clothes_response = requests.get(PRODUCT_SERVICE_CLOTHES_URL + f'/search_clothes?key={key}')
    mobile_response = requests.get(PRODUCT_SERVICE_MOBILE_URL + f'/search_mobiles?key={key}')
    result = []
    if book_response.status_code == 200:
        result += book_response.json()
    if clothes_response.status_code == 200:
        result += clothes_response.json()
    if mobile_response.status_code == 200:
        result += mobile_response.json()
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
    response = requests.get(PRODUCT_SERVICE_BOOK_URL + f'/search_books?key={key}')
    return Response(response.json())


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
    response = requests.get(PRODUCT_SERVICE_CLOTHES_URL + f'/search_clothes?key={key}')
    return Response(response.json())


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
    response = requests.get(PRODUCT_SERVICE_MOBILE_URL + f'/search_mobiles?key={key}')
    return Response(response.json())
