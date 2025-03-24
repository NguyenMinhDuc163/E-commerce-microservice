from rest_framework import serializers
from .models import Review

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'
        extra_kwargs = {
            'id': {'help_text': 'ID của đánh giá'},
            'user_id': {'help_text': 'ID của người dùng'},
            'product_id': {'help_text': 'ID của sản phẩm'},
            'product_type': {'help_text': 'Loại sản phẩm (book, mobile, clothes)'},
            'rating': {'help_text': 'Điểm đánh giá (1-5)'},
            'comment': {'help_text': 'Nội dung đánh giá'},
            'created_at': {'help_text': 'Thời gian tạo đánh giá'},
            'updated_at': {'help_text': 'Thời gian cập nhật đánh giá'}
        } 