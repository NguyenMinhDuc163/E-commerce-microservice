from rest_framework import serializers
from .models import Book, Author, Publisher, Category


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'
        extra_kwargs = {
            'id': {'help_text': 'ID của sách'},
            'title': {'help_text': 'Tiêu đề sách'},
            'author': {'help_text': 'Tác giả của sách'},
            'publisher': {'help_text': 'Nhà xuất bản'},
            'categories': {'help_text': 'Thể loại sách'},
            'price': {'help_text': 'Giá sách'},
            'description': {'help_text': 'Mô tả sách'},
            'image': {'help_text': 'Ảnh bìa sách'},
            'created_at': {'help_text': 'Thời gian tạo'},
            'updated_at': {'help_text': 'Thời gian cập nhật'}
        }


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'
        extra_kwargs = {
            'id': {'help_text': 'ID của tác giả'},
            'name': {'help_text': 'Tên tác giả'},
            'description': {'help_text': 'Mô tả tác giả'},
            'created_at': {'help_text': 'Thời gian tạo'},
            'updated_at': {'help_text': 'Thời gian cập nhật'}
        }
