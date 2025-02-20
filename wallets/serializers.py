# serializers.py
from rest_framework import serializers
from .models import Wallet, Withdrawal

class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ['wallet_id', 'merchant', 'amount', 'currency', 'createdAt', 'updatedAt']
        
    def validate(self, data):
        """Ensure admin privileges when modifying sensitive fields."""
        request = self.context.get('request')
        if request and not request.user.is_superuser:
            raise serializers.ValidationError("Only superusers can modify wallet details.")
        return data


class WithdrawalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Withdrawal
        fields = ['sn', 'withdrawal_id', 'merchant', 'amount', 'initial_balance', 'final_balance', 'status', 'createdAt', 'updatedAt']

    def validate(self, data):
        """Ensure the withdrawal amount does not exceed wallet balance."""
        merchant = data.get("merchant")
        amount = data.get("amount")

        # Get merchant's wallet
        wallet = Wallet.objects.filter(merchant=merchant).first()
        if not wallet:
            raise serializers.ValidationError("Merchant wallet not found.")
        
        # Ensure wallet has enough funds
        if amount > wallet.amount:
            raise serializers.ValidationError("Insufficient balance.")

        return data