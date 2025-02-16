from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from authentication.models import Merchant
from .models import AuditLog
from .serializers import MerchantSerializer, AuditLogSerializer

class IsSuperAdmin(IsAuthenticated):
    """Ensures that only superadmin users can access these views."""
    def has_permission(self, request, view):
        return bool(request.user and request.user.role == "superadmin")

# ✅ View all merchants
class MerchantListView(generics.ListAPIView):
    queryset = Merchant.objects.filter(role="merchant")  # ✅ Only merchants
    serializer_class = MerchantSerializer
    permission_classes = [IsSuperAdmin]

# ✅ Retrieve a specific merchant
class MerchantDetailView(generics.RetrieveAPIView):
    queryset = Merchant.objects.filter(role="merchant")
    serializer_class = MerchantSerializer
    permission_classes = [IsSuperAdmin]
    lookup_field = "merchant_id"

# ✅ Update a merchant
class MerchantUpdateView(generics.UpdateAPIView):
    queryset = Merchant.objects.filter(role="merchant")
    serializer_class = MerchantSerializer
    permission_classes = [IsSuperAdmin]
    lookup_field = "merchant_id"

    def perform_update(self, serializer):
        merchant = serializer.save()
        AuditLog.objects.create(admin=self.request.user, action=f"Updated merchant {merchant.email}")

# ✅ Delete a merchant
class MerchantDeleteView(generics.DestroyAPIView):
    queryset = Merchant.objects.filter(role="merchant")
    serializer_class = MerchantSerializer
    permission_classes = [IsSuperAdmin]
    lookup_field = "merchant_id"

    def perform_destroy(self, instance):
        AuditLog.objects.create(admin=self.request.user, action=f"Deleted merchant {instance.email}")
        instance.delete()

# ✅ View admin actions (audit logs)
class AuditLogListView(generics.ListAPIView):
    queryset = AuditLog.objects.all().order_by("-created_at")
    serializer_class = AuditLogSerializer
    permission_classes = [IsSuperAdmin]
