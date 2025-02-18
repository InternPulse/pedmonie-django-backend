from django.db import models

# Create your models here.
import uuid
from authentication.models import Merchant

class PaymentGateway(models.Model):
    gateway_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    gateway_logo = models.ImageField(upload_to='payment_gateway_logos/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class MerchantPaymentGateway(models.Model):
    gateway_payment_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    gateway = models.ForeignKey(PaymentGateway, on_delete=models.CASCADE)
    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE, limit_choices_to={'role': 'merchant'})
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.merchant.business_name} - {self.gateway.name}"
