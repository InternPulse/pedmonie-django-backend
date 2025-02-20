from django.db import models

from django.db import models
class Transaction(models.Model):
    transaction_id = models.UUIDField(primary_key=True)
    order_id = models.UUIDField()
    merchant_id = models.UUIDField()
    gateway_name = models.CharField(max_length=50)
    gateway_transaction_identifier = models.CharField(max_length=50)
    payment_channel = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=19, decimal_places=4)
    status = models.CharField(max_length=10, choices=[("pending", "pending"), ("successful", "successful"), ("failed", "failed")])
    currency = models.CharField(max_length=50, default="NGN")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'transactions'