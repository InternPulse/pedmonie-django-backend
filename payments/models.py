from django.db import models

# Create your models here.
import uuid
from authentication.models import Merchant

class PaymentGateway(models.Model):
    gateway_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sn = models.CharField(max_length=50,unique=True, db_index=True, verbose_name="Serial Number", blank=True)
    name = models.CharField(max_length=50)
    gateway_logo = models.ImageField(upload_to='payment_gateway_logos/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    def save(self, *args, **kwargs):
        if not self.sn:  # Only assign if 'sn' is empty
            last_PG = PaymentGateway.objects.order_by('-sn').first()
            if last_PG and last_PG.sn.isdigit():
                self.sn = str(int(last_PG.sn) + 1)
            else:
                self.sn = "1"  # Start from 1 if no records exist
        super().save(*args, **kwargs)

class MerchantPaymentGateway(models.Model):
    gateway_payment_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sn = models.CharField(max_length=50,unique=True, db_index=True, verbose_name="Serial Number", blank=True)
    gateway = models.ForeignKey(PaymentGateway, on_delete=models.CASCADE)
    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE, limit_choices_to={'role': 'merchant'})
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.merchant.business_name} - {self.gateway.name}"
    def save(self, *args, **kwargs):
        if not self.sn:  # Only assign if 'sn' is empty
            last_sn = MerchantPaymentGateway.objects.order_by('-gateway_id').first()
            if last_sn and last_sn.sn.isdigit():
                self.sn = str(int(last_sn.sn) + 1)
            else:
                self.sn = "1"  # Start from 1 if no records exist
        super().save(*args, **kwargs)

    def __str__(self):
        return self.sn
