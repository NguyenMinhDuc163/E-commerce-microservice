from rest_framework import serializers
from .models import PaymentStatus

class PaymentStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentStatus
        fields = '__all__'
        extra_kwargs = {
            'id': {'help_text': 'ID của thanh toán'},
            'user_id': {'help_text': 'ID của người dùng'},
            'order_item_id': {'help_text': 'ID của đơn hàng'},
            'price': {'help_text': 'Tổng giá trị thanh toán'},
            'status': {'help_text': 'Trạng thái thanh toán (Pending/Success/Failed)'},
            'payment_type': {'help_text': 'Loại thanh toán'},
            'payment_date': {'help_text': 'Ngày thanh toán'}
        }
