from rest_framework import serializers
from .models import Wallet

class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ['wallet_id', 'merchant', 'amount', 'currency', 'created_at', 'updated_at']
        
    def validate(self, data):
        """Ensure admin privileges when modifying sensitive fields."""
        request = self.context.get('request')
        if request and not request.user.is_superuser:
            raise serializers.ValidationError("Only superusers can modify wallet details.")
        return data
