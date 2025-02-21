from django.db import models
from authentication.models import Merchant
import uuid

class Order(models.Model):
    order_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sn = models.CharField(max_length=50,unique=True, db_index=True, verbose_name="Serial Number", blank=True)
    gateway_name = models.CharField(max_length=50)
    merchant_id = models.ForeignKey(Merchant, on_delete=models.PROTECT, related_name='orders')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3)
    order_status = models.CharField(max_length=20,default='pending')
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.sn:  # Only assign if 'sn' is empty
            last_order = Order.objects.exclude(sn='').order_by(models.functions.Cast('sn', models.IntegerField()).desc()).first()
            if last_order and last_order.sn.isdigit():
                self.sn = str(int(last_order.sn) + 1)
            else:
                self.sn = "1"  # Start from 1 if no records exist
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['createdAt']
        db_table = 'orders'

    
