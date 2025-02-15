from rest_framework import serializers
from authentication.models import Merchant
from authentication.serializers import AdminSerializer  
from .models import AuditLog

class MerchantDashboardSerializer(AdminSerializer):  
    """Serializer for displaying merchant details in the dashboard (admin only)."""

    class Meta(AdminSerializer.Meta):  
        fields = AdminSerializer.Meta.fields + ['total_balance', 'created_at']
        read_only_fields = ['total_balance', 'created_at']

class AuditLogSerializer(serializers.ModelSerializer):
    """Serializes admin audit logs."""
    admin_email = serializers.EmailField(source="admin.email", read_only=True)

    class Meta:
        model = AuditLog
        fields = ["log_id", "admin_email", "action", "created_at"]
