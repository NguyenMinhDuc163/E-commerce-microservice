from django.db import models

class PaymentStatus(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    order_item_id = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    status = models.CharField(max_length=20, default="Pending")
    payment_type = models.CharField(max_length=20)
    payment_date = models.DateField(null=True)
