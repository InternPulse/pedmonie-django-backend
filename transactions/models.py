from django.db import models
from django.db import models
import uuid 
from authentication.models import Merchant
from orders.models import Order


class Transaction(models.Model):
    transaction_id = models.UUIDField(primary_key=True)
    sn = models.IntegerField(unique=True, db_index=True, verbose_name="Serial Number")
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_transactions')
    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE, related_name='transactions')
    gateway_name = models.CharField(max_length=50)
    gateway_transaction_identifier = models.CharField(max_length=50)
    payment_channel = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=19, decimal_places=4)
    status = models.CharField(max_length=20, choices=[
        ("pending", "Pending"),
        ("successful", "Successful"),
        ("failed", "Failed")
    ], default="pending")
    currency = models.CharField(max_length=50, blank=False)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'transactions'

    def save(self, *args, **kwargs):
        if not self.sn:  # Only assign if 'sn' is empty
            last_sn = Transaction.objects.order_by('-sn').first()
            self.sn = last_sn.sn + 1 if last_sn else 1
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Transaction {self.transaction_id} - {self.status}"

        
