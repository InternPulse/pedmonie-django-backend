from rest_framework import serializers
from authentication.models import User
from .models import AuditLog 

# Serialize Merchant Data for Admin Dashboard
class MerchantSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "merchant_id", "first_name", "last_name", "business_name", "email",
            "phone", "total_balance", "is_email_verified", "is_kyc_verified",
            "created_at"
        ]
        read_only_fields = ["merchant_id", "created_at"]

# Serialize Audit Logs
class AuditLogSerializer(serializers.ModelSerializer):
    admin_email = serializers.EmailField(source="admin.email", read_only=True)

    class Meta:
        model = AuditLog
        fields = ["log_id", "admin_email", "action", "created_at"]