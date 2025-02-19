from django.db import models

class Withdrawal(models.Model):
    merchant_id = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
class PaymentGateway(models.Model):
    name = models.CharField(max_length=255)
    # Add any other fields here

class MerchantPaymentGateway(models.Model):
    merchant_id = models.CharField(max_length=255)
    payment_gateway = models.ForeignKey(PaymentGateway, on_delete=models.CASCADE)
    # Add any other fields here

