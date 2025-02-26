import uuid
from django.db import models
from django.utils import timezone
from authentication.models import Merchant

class Wallet(models.Model):
    wallet_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sn = models.IntegerField(max_length=50,unique=True, db_index=True, verbose_name="Serial Number", blank=True)
    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE, related_name='wallet')
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    currency = models.CharField(max_length=3, default="NGN")
    createdAt = models.DateTimeField(default=timezone.now)
    updatedAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Wallet {self.wallet_id} - {self.merchant.email}"
    
    def save(self, *args, **kwargs):
        if not self.sn:  # Only assign if 'sn' is empty
            last_sn = Wallet.objects.order_by('-sn').first()
            self.sn = last_sn.sn + 1 if last_sn else 1
        super().save(*args, **kwargs)


    class Meta:
        db_table = 'wallets'
        ordering = ["createdAt"]

    def __str__(self):
        return f"Wallet {self.wallet_id} - {self.merchant.email}"
        


class Withdrawal(models.Model):
    withdrawal_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sn = models.IntegerField(unique=True, db_index=True, verbose_name="Serial Number", blank=True)
    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE, related_name='withdrawal')
    amount = models.DecimalField(max_digits=19, decimal_places=4)
    initial_balance = models.DecimalField(max_digits=19, decimal_places=4)
    final_balance = models.DecimalField(max_digits=19, decimal_places=4)
    status = models.CharField(max_length=20, choices=[
        ("pending", "Pending"),
        ("successful", "Successful"),
        ("failed", "Failed")
    ], default="pending")
    createdAt = models.DateTimeField(default=timezone.now)
    updatedAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Withdrawal {self.withdrawal_id} - {self.merchant.email} - {self.status}"
    
    def save(self, *args, **kwargs):
        if not self.sn:  # Only assign if 'sn' is empty
            last_sn = Withdrawal.objects.order_by('-sn').first()
            self.sn = last_sn.sn + 1 if last_sn else 1
        super().save(*args, **kwargs)
   
    class Meta:
        db_table = 'withdrawals'
        ordering = ["createdAt"]
