from bson import ObjectId
from django.db.models import Q
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Book, Author, Publisher, Category
from .serializers import BookSerializer
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes


@extend_schema(
    summary="Lấy danh sách tất cả sách",
    description="API để lấy danh sách tất cả các sách trong hệ thống",
    responses={200: BookSerializer(many=True)}
)
@api_view(['GET'])
def get_books(request):
    books = Book.objects.all()
    serializer = BookSerializer(books, many=True)
    data = serializer.data
    for book in data:
        # Handle both string names and ObjectId references
        try:
            # If author is ObjectId, get the name
            book['author'] = Author.objects.get(pk=ObjectId(book['author'])).name
        except:
            # If author is already a string name, keep it as is
            pass
            
        try:
            # If publisher is ObjectId, get the name
            book['publisher'] = Publisher.objects.get(pk=ObjectId(book['publisher'])).name
        except:
            # If publisher is already a string name, keep it as is
            pass
            
        try:
            # If categories is ObjectId, get the name
            book['categories'] = Category.objects.get(pk=ObjectId(book['categories'])).name
        except:
            # If categories is already a string name, keep it as is
            pass
    return Response(data)


@extend_schema(
    summary="Lấy chi tiết sách",
    description="API để lấy thông tin chi tiết của một cuốn sách",
    parameters=[
        OpenApiParameter(
            name='pk',
            type=OpenApiTypes.STR,
            description='ID của sách'
        )
    ],
    responses={
        200: BookSerializer,
        404: {'type': 'object', 'properties': {'error': {'type': 'string'}}}
    }
)
@api_view(['GET'])
def get_book(request, pk):
    try:
        book = Book.objects.get(pk=ObjectId(pk))
        serializer = BookSerializer(book)
        data = serializer.data
        
        # Handle both string names and ObjectId references
        try:
            data['author'] = Author.objects.get(pk=ObjectId(book.author)).name
        except:
            data['author'] = book.author  # Already a string name
            
        try:
            data['publisher'] = Publisher.objects.get(pk=ObjectId(book.publisher)).name
        except:
            data['publisher'] = book.publisher  # Already a string name
            
        try:
            data['categories'] = Category.objects.get(pk=ObjectId(book.categories)).name
        except:
            data['categories'] = book.categories  # Already a string name
            
        return Response(data)
    except Book.DoesNotExist:
        return Response({'error': 'Book not found'}, status=404)


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
    responses={200: BookSerializer(many=True)}
)
@api_view(['GET'])
def search_books(request):
    key = request.query_params.get('key', '')
    if key:
        authors = Author.objects.filter(
            Q(name__icontains=key)
        )
        publishers = Publisher.objects.filter(
            Q(name__icontains=key)
        )
        books = Book.objects.filter(
            Q(title__icontains=key) |
            Q(author__in=[str(author.pk) for author in authors]) |
            Q(publisher__in=[str(publisher.pk) for publisher in publishers])
        )
        books = list(books)
    else:
        books = Book.objects.all()

    serializer = BookSerializer(books, many=True)
    data = serializer.data
    for book in data:
        # Handle both string names and ObjectId references
        try:
            book['author'] = Author.objects.get(pk=ObjectId(book['author'])).name
        except:
            pass  # Already a string name
            
        try:
            book['publisher'] = Publisher.objects.get(pk=ObjectId(book['publisher'])).name
        except:
            pass  # Already a string name
            
        try:
            book['categories'] = Category.objects.get(pk=ObjectId(book['categories'])).name
        except:
            pass  # Already a string name
    return Response(data)
