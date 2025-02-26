from django.db import models
from authentication.models import Merchant
import uuid

class Order(models.Model):
    sn = models.IntegerField(unique=True, db_index=True, verbose_name="Serial Number")
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

    def save(self, *args, **kwargs):
        if not self.sn:  # Only assign if 'sn' is empty
            last_order = Order.objects.order_by('-sn').first()
            self.sn = last_order.sn + 1 if last_order else 1
        super().save(*args, **kwargs)


    class Meta:
        ordering = ['createdAt']
        db_table = 'orders'

    
