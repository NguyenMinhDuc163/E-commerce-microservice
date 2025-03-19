from rest_framework import serializers

from .models import CartItem


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = '__all__'

    def create(self, validated_data):
        user_id = validated_data['user_id']
        product_id = validated_data['product_id']
        type = validated_data['type']
        # Kiểm tra xem sản phẩm đã tồn tại trong giỏ hàng chưa nếu có thì cộng thêm số lượng
        cart_item = CartItem.objects.filter(user_id=user_id, product_id=product_id, type=type).first()
        if cart_item:
            cart_item.quantity += validated_data['quantity']
            cart_item.save()
            return cart_item
        return CartItem.objects.create(**validated_data)