from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from .models import Review
from .serializers import ReviewSerializer
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes

class ReviewListView(APIView):
    @extend_schema(
        summary="Lấy danh sách đánh giá",
        description="API để lấy danh sách tất cả các đánh giá",
        parameters=[
            OpenApiParameter(
                name='product_id',
                type=OpenApiTypes.STR,
                description='ID của sản phẩm'
            ),
            OpenApiParameter(
                name='product_type',
                type=OpenApiTypes.STR,
                description='Loại sản phẩm (book, mobile, clothes)'
            )
        ],
        responses={200: ReviewSerializer(many=True)}
    )
    def get(self, request):
        product_id = request.query_params.get('product_id')
        product_type = request.query_params.get('product_type')
        
        reviews = Review.objects.all()
        if product_id:
            reviews = reviews.filter(product_id=product_id)
        if product_type:
            reviews = reviews.filter(product_type=product_type)
            
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)

class ReviewCreateView(APIView):
    @extend_schema(
        summary="Tạo đánh giá mới",
        description="API để tạo một đánh giá mới cho sản phẩm",
        request={
            'application/json': {
                'type': 'object',
                'properties': {
                    'user_id': {'type': 'integer'},
                    'product_id': {'type': 'string'},
                    'product_type': {'type': 'string', 'enum': ['book', 'mobile', 'clothes']},
                    'rating': {'type': 'integer', 'minimum': 1, 'maximum': 5},
                    'comment': {'type': 'string'}
                },
                'required': ['user_id', 'product_id', 'product_type', 'rating', 'comment']
            }
        },
        responses={
            201: ReviewSerializer,
            400: {'type': 'object', 'properties': {'error': {'type': 'string'}}}
        }
    )
    @csrf_exempt
    def post(self, request):
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ReviewDetailView(APIView):
    @extend_schema(
        summary="Lấy chi tiết đánh giá",
        description="API để lấy thông tin chi tiết của một đánh giá",
        parameters=[
            OpenApiParameter(
                name='pk',
                type=OpenApiTypes.INT,
                description='ID của đánh giá'
            )
        ],
        responses={
            200: ReviewSerializer,
            404: {'type': 'object', 'properties': {'error': {'type': 'string'}}}
        }
    )
    def get(self, request, pk):
        try:
            review = Review.objects.get(pk=pk)
            serializer = ReviewSerializer(review)
            return Response(serializer.data)
        except Review.DoesNotExist:
            return Response({'error': 'Review not found'}, status=status.HTTP_404_NOT_FOUND) 