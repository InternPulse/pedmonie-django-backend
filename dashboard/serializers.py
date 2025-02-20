from rest_framework import serializers
from authentication.models import Merchant
from .models import AuditLog

class MerchantSerializer(serializers.ModelSerializer):
    """Used to serialize merchant data for the admin dashboard."""
    class Meta:
        model = Merchant
        fields = [
            "merchant_id", "first_name", "last_name", "business_name", "email",
            "phone", "total_balance", "is_email_verified", "is_kyc_verified",
            "createdAt"
        ]
        read_only_fields = ["merchant_id", "createdAt"]

class AuditLogSerializer(serializers.ModelSerializer):
    """Serializes admin audit logs."""
    admin_email = serializers.EmailField(source="admin.email", read_only=True)  # Get admin email from Merchant model

    class Meta:
        model = AuditLog
        fields = ["log_id", "admin_email", "action", "created_at"]