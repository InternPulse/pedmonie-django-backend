from django.db import models
from authentication.models import Merchant
import uuid

class Order(models.Model):
    sn = models.AutoField(unique=True, db_index=True, verbose_name="Serial Number")
    order_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    gateway_name = models.CharField(max_length=50)
    merchant = models.ForeignKey(Merchant, on_delete=models.PROTECT, related_name='orders')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3)
    order_status = models.CharField(max_length=20, choices=[
        ("pending", "Pending"),
        ("successful", "Successful"),
        ("failed", "Failed")
    ], default="pending")
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)


    class Meta:
        ordering = ['createdAt']
        db_table = 'orders'

    
