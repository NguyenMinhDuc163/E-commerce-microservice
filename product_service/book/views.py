from bson import ObjectId
from django.db.models import Q
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Book, Author, Publisher, Category
from .serializers import BookSerializer


@api_view(['GET'])
def get_books(request):
    books = Book.objects.all()
    serializer = BookSerializer(books, many=True)
    data = serializer.data
    for book in data:
        book['author'] = Author.objects.get(pk=ObjectId(book['author'])).name
        book['publisher'] = Publisher.objects.get(pk=ObjectId(book['publisher'])).name
        book['categories'] = Category.objects.get(pk=ObjectId(book['categories'])).name
    return Response(serializer.data)


@api_view(['GET'])
def get_book(request, pk):
    try:
        book = Book.objects.get(pk=ObjectId(pk))
        serializer = BookSerializer(book)
        data = serializer.data
        data['author'] = Author.objects.get(pk=ObjectId(book.author)).name
        data['publisher'] = Publisher.objects.get(pk=ObjectId(book.publisher)).name
        data['categories'] = Category.objects.get(pk=ObjectId(book.categories)).name
        return Response(data)
    except Book.DoesNotExist:
        return Response({'error': 'Book not found'}, status=404)


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
        book['author'] = Author.objects.get(pk=ObjectId(book['author'])).name
        book['publisher'] = Publisher.objects.get(pk=ObjectId(book['publisher'])).name
        book['categories'] = Category.objects.get(pk=ObjectId(book['categories'])).name
    return Response(data)
