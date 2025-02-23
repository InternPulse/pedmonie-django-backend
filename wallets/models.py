import uuid
from django.db import models
from django.utils import timezone
from authentication.models import Merchant

class Wallet(models.Model):
    wallet_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sn = models.CharField(max_length=50,unique=True, db_index=True, verbose_name="Serial Number", blank=True)
    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE, related_name='wallets')
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    currency = models.CharField(max_length=3, default="NGN")
    createdAt = models.DateTimeField(default=timezone.now)
    updatedAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Wallet {self.wallet_id} - {self.merchant.email}"
    
    def save(self, *args, **kwargs):
        if not self.sn:  # Only assign if 'sn' is empty
            last_wallet = Wallet.objects.exclude(sn='').order_by(models.functions.Cast('sn', models.IntegerField()).desc()).first()
            if last_wallet and last_wallet.sn.isdigit():
                self.sn = str(int(last_wallet.sn) + 1)
            else:
                self.sn = "1"  # Start from 1 if no records exist
        super().save(*args, **kwargs)


    class Meta:
        db_table = 'wallets'
        ordering = ["createdAt"]

    def __str__(self):
        return f"Wallet {self.wallet_id} - {self.merchant.email}"
        


class Withdrawal(models.Model):
    withdrawal_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sn = models.CharField(max_length=50,unique=True, db_index=True, verbose_name="Serial Number", blank=True)
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
            last_withdrawal = Withdrawal.objects.exclude(sn='').order_by(models.functions.Cast('sn', models.IntegerField()).desc()).first()
            if last_withdrawal and last_withdrawal.sn.isdigit():
                self.sn = str(int(last_withdrawal.sn) + 1)
            else:
                self.sn = "1"  # Start from 1 if no records exist
        super().save(*args, **kwargs)

   
    class Meta:
        db_table = 'withdrawals'
        ordering = ["createdAt"]
