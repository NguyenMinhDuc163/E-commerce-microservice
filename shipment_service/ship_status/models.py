from django.db import models

class Shipment(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    order_item_id = models.IntegerField()
    username = models.CharField(max_length=50) # ten nguoi nhan
    address = models.CharField(max_length=100) # dia chi nguoi nhan
    phone = models.CharField(max_length=10) # so nguoi nhan
    shipment_status = models.CharField(max_length=50) # chưa vận chuyển , đang van chuyen, van chuyen thanh cong
    shipment_type = models.CharField(max_length=50) # loại vận chuyen: hoa toc, nhanh, tiet kiem
    price = models.IntegerField(null=True) # hoa toc: 50, nhanh: 20, tiet kiem; 10