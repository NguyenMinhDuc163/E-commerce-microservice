from rest_framework import serializers
from .models import Shipment

class ShipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shipment
        fields = '__all__'

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
