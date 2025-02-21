from django.db import models
from django.db import models
import uuid  


class Transaction(models.Model):
    transaction_id = models.UUIDField(primary_key=True)
    sn = models.CharField(max_length=50,unique=True, db_index=True, verbose_name="Serial Number", blank=True)
    order_id = models.UUIDField()
    merchant_id = models.UUIDField()
    gateway_name = models.CharField(max_length=50)
    gateway_transaction_identifier = models.CharField(max_length=50)
    payment_channel = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=19, decimal_places=4)
    status = models.CharField(max_length=10, choices=[("pending", "Pending"), ("successful", "Successful"), ("failed", "Failed")])
    currency = models.CharField(max_length=50, default="NGN")
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'transactions'

    def __str__(self):
        return f"Transaction {self.transaction_id} - {self.status}"
    
    def save(self, *args, **kwargs):
        if not self.sn:  # Only assign if 'sn' is empty
            last_transaction = Transaction.objects.exclude(sn='').order_by(models.functions.Cast('sn', models.IntegerField()).desc()).first()
            if last_transaction and last_transaction.sn.isdigit():
                self.sn = str(int(last_transaction.sn) + 1)
            else:
                self.sn = "1"  # Start from 1 if no records exist
        super().save(*args, **kwargs)
        
