from rest_framework import serializers
from .models import PaymentGateway, MerchantPaymentGateway


class PaymentGatewaySerializer(serializers.ModelSerializer):
    """Serializer for payment gateways"""

    class Meta:
        model = PaymentGateway
        fields = "__all__"


class MerchantPaymentGatewaySerializer(serializers.ModelSerializer):
    """Serializer for a merchant's payment gateways"""

    class Meta:
        model = MerchantPaymentGateway
        fields = "__all__"

    def update(self, instance, validated_data):
        """
        Custom update method to modify a merchant's enabled payment gateways.
        """
        instance.payment_gateways = validated_data.get("payment_gateways", instance.payment_gateways)
        instance.save()
        return instance
