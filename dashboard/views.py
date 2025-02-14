from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from authentication.models import User
from .models import AuditLog
from .serializers import MerchantSerializer, AuditLogSerializer

# Permission: Only superadmins can manage merchants
class IsSuperAdmin(IsAuthenticated):
    def has_permission(self, request, view):
        return bool(request.user and request.user.role == "superadmin")

# Retrieve All Merchants
class MerchantListView(generics.ListAPIView):
    queryset = User.objects.filter(role="merchant")
    serializer_class = MerchantSerializer
    permission_classes = [IsSuperAdmin]

# Retrieve a Specific Merchant
class MerchantDetailView(generics.RetrieveAPIView):
    queryset = User.objects.filter(role="merchant")
    serializer_class = MerchantSerializer
    permission_classes = [IsSuperAdmin]
    lookup_field = "merchant_id"

# Update Merchant Details
class MerchantUpdateView(generics.UpdateAPIView):
    queryset = User.objects.filter(role="merchant")
    serializer_class = MerchantSerializer
    permission_classes = [IsSuperAdmin]
    lookup_field = "merchant_id"

    def perform_update(self, serializer):
        merchant = serializer.save()
        AuditLog.objects.create(admin=self.request.user, action=f"Updated merchant {merchant.email}")

# Delete Merchant
class MerchantDeleteView(generics.DestroyAPIView):
    queryset = User.objects.filter(role="merchant")
    serializer_class = MerchantSerializer
    permission_classes = [IsSuperAdmin]
    lookup_field = "merchant_id"

    def perform_destroy(self, instance):
        AuditLog.objects.create(admin=self.request.user, action=f"Deleted merchant {instance.email}")
        instance.delete()

# View Audit Logs
class AuditLogListView(generics.ListAPIView):
    queryset = AuditLog.objects.all().order_by("-created_at")
    serializer_class = AuditLogSerializer
    permission_classes = [IsSuperAdmin]