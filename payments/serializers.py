from rest_framework import serializers
from .models import PaymentGateway, MerchantPaymentGateway

class PaymentGatewaySerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentGateway
        fields = '__all__'

class MerchantPaymentGatewaySerializer(serializers.ModelSerializer):
    class Meta:
        model = MerchantPaymentGateway
        fields = '__all__'
