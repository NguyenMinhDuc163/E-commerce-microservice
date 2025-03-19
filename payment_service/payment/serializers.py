from rest_framework import serializers
from .models import PaymentStatus

class PaymentStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentStatus
        fields = '__all__'
