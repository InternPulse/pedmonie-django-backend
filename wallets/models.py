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
            last_sn = Wallet.objects.order_by('-wallet_id').first()
            if last_sn and last_sn.sn.isdigit():
                self.sn = str(int(last_sn.sn) + 1)
            else:
                self.sn = "1"  # Start from 1 if no records exist
        super().save(*args, **kwargs)

    def __str__(self):
        return self.sn

    class Meta:
        ordering = ["-createdAt"]
    