from rest_framework import serializers
from .models import OrderItem

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'

class UpdateOrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['quantity', 'status', 'updated_at', 'payment_id', 'shipment_id']

    def update(self, instance, validated_data):
        instance.quantity = validated_data.get('quantity', instance.quantity)
        instance.status = validated_data.get('status', instance.status)
        instance.updated_at = validated_data.get('updated_at', instance.updated_at)
        instance.payment_id = validated_data.get('payment_id', instance.payment_id)
        instance.shipment_id = validated_data.get('shipment_id', instance.shipment_id)
        instance.save()
        return instance
