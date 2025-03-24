from rest_framework import serializers
from .models import Shipment

class ShipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shipment
        fields = '__all__'
        extra_kwargs = {
            'id': {'help_text': 'ID của đơn vận chuyển'},
            'user_id': {'help_text': 'ID của người dùng'},
            'order_item_id': {'help_text': 'ID của đơn hàng'},
            'shipment_type': {'help_text': 'Loại vận chuyển (EXPRESS/FAST/ECONOMICAL)'},
            'shipment_status': {'help_text': 'Trạng thái vận chuyển'},
            'price': {'help_text': 'Giá vận chuyển'},
            'created_at': {'help_text': 'Thời gian tạo đơn'},
            'updated_at': {'help_text': 'Thời gian cập nhật đơn'}
        }

    def create(self, validated_data):
        shipment_type = validated_data.get('shipment_type')
        validated_data['price'] = self.calculate_price(shipment_type)
        return super().create(validated_data)

    def calculate_price(self, shipment_type):
        if shipment_type == 'EXPRESS': # hoa toc
            return 50
        elif shipment_type == 'FAST': # nhanh
            return 20
        elif shipment_type == 'ECONOMICAL ': # tiêt kiêm
            return 10
        return 0
