import uuid
from django.db import models
from django.utils import timezone
from authentication.models import Merchant  # Adjust the import if necessary

class Wallet(models.Model):
    wallet_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    currency = models.CharField(max_length=3, default="NGN")
    createdAt = models.DateTimeField(default=timezone.now)
    updatedAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Wallet {self.wallet_id} - {self.merchant.email}"

    class Meta:
        ordering = ["-createdAt"]