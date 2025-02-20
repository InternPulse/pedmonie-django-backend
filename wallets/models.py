import uuid
from django.db import models
from django.utils import timezone
from authentication.models import Merchant  # Adjust the import if necessary

class Wallet(models.Model):
    wallet_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sn = models.CharField(max_length=50,unique=True, db_index=True, verbose_name="Serial Number", blank=True)
    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    currency = models.CharField(max_length=3, default="NGN")
    createdAt = models.DateTimeField(default=timezone.now)
    updatedAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Wallet {self.wallet_id} - {self.merchant.email}"
    
    def save(self, *args, **kwargs):
        if not self.sn:  # Only assign if 'sn' is empty
            last_wallet = Wallet.objects.order_by('-sn').first()
            if last_wallet and last_wallet.sn.isdigit():
                self.sn = str(int(last_wallet.sn) + 1)
            else:
                self.sn = "1"  # Start from 1 if no records exist
        super().save(*args, **kwargs)

    class Meta:
        ordering = ["-createdAt"]
    