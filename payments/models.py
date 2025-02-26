import uuid
from django.db import models
from authentication.models import Merchant  # Import Merchant model

class PaymentGateway(models.Model):
    """
    Model for storing available payment gateways.
    """
    sn = models.IntegerField(unique=True, db_index=True, verbose_name="Serial Number")
    gateway_id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    gateway_name = models.CharField(max_length=100, unique=True)
    gateway_logo = models.ImageField(upload_to="gateway_logo/", null=True, blank=True)
    is_active = models.BooleanField(default=False)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)



    class Meta:
        db_table = "paymentgateways"  # Matches Sequelize table name

    def save(self, *args, **kwargs):
        if not self.sn:  # Only assign if 'sn' is empty
            last_sn = PaymentGateway.objects.order_by('-sn').first()
            self.sn = last_sn.sn + 1 if last_sn else 1
        super().save(*args, **kwargs)

    



class MerchantPaymentGateway(models.Model):
    """
    Model for storing a merchant's enabled payment gateways.
    """
    sn = models.IntegerField(primary_key=True, unique=True, db_index=True, verbose_name="Serial Number")  # Matches Sequelize's `autoIncrement: true`
    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE, related_name='merchant_payment_gateway')
    payment_gateways = models.JSONField(blank=False)  # Store JSON data for active payment gateways
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "merchant_payment_gateway"  # Matches Sequelize table name

    def save(self, *args, **kwargs):
        if not self.sn:  # Only assign if 'sn' is empty
            last_sn = MerchantPaymentGateway.objects.exclude(sn='').order_by('-sn').first()
            self.sn = last_sn.sn + 1 if last_sn else 1
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.merchant.business_name}'s Payment Gateways"
