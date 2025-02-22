import uuid
from django.db import models
from authentication.models import Merchant  # Import Merchant model

class PaymentGateway(models.Model):
    """
    Model for storing available payment gateways.
    """
    sn = models.CharField(max_length=50,unique=True, db_index=True, verbose_name="Serial Number", blank=True)
    gateway_id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    gateway_name = models.CharField(max_length=100, unique=True)
    gateway_logo = models.CharField(max_length=255)
    is_active = models.BooleanField(default=False)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)


    def save(self, *args, **kwargs):
        if not self.sn:  # Only assign if 'sn' is empty
            last_PG = PaymentGateway.objects.exclude(sn='').order_by(models.functions.Cast('sn', models.IntegerField()).desc()).first()
            if last_PG and last_PG.sn.isdigit():
                self.sn = str(int(last_PG.sn) + 1)
            else:
                self.sn = "1"  # Start from 1 if no records exist
        super().save(*args, **kwargs)

    class Meta:
        db_table = "paymentgateways"  # Matches Sequelize table name

    



class MerchantPaymentGateway(models.Model):
    """
    Model for storing a merchant's enabled payment gateways.
    """
    sn = models.AutoField(primary_key=True)  # Matches Sequelize's `autoIncrement: true`
    merchant_id = models.OneToOneField(Merchant, on_delete=models.CASCADE, related_name="merchant_gateways")
    payment_gateways = models.JSONField(default=dict)  # Store JSON data for active payment gateways

    class Meta:
        db_table = "merchant_payment_gateway"  # Matches Sequelize table name

    def __str__(self):
        return f"{self.merchant.business_name}'s Payment Gateways"
