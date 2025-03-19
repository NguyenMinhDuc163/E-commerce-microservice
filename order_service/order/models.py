from django.db import models

class OrderItem(models.Model):
    order_item_id = models.AutoField(primary_key=True)
    user_id = models.IntegerField(null=False)
    product_id = models.CharField(max_length=255, null=False)  # thêm max_length
    type = models.CharField(max_length=10, null=False)
    quantity = models.IntegerField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    payment_id = models.IntegerField(null=True)
    shipment_id = models.IntegerField(null=True)
    total = models.IntegerField(null=True)
