from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from authentication.models import Merchant
from authentication.serializers import AdminSerializer
from dashboard.models import AuditLog
from dashboard.serializers import AuditLogSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication

# Admin gets all merchants
class MerchantListView(APIView):
    """List all merchants (Admin only)."""
    authentication_classes = JWTAuthentication
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Retrieve all merchants."""
        merchants = Merchant.objects.all()
        serializer = AdminSerializer(merchants, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

#  Admin gets a specific merchant, updates or deletes them
class MerchantDetailView(APIView):
    """Retrieve, update, or delete a single merchant (Admin only)."""
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, merchant_id):
        """Retrieve a merchant by ID."""
        try:
            merchant = Merchant.objects.get(merchant_id=merchant_id)
            serializer = AdminSerializer(merchant)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Merchant.DoesNotExist:
            return Response({"error": "Merchant not found"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, merchant_id):
        """Update a merchant's details."""
        try:
            merchant = Merchant.objects.get(merchant_id=merchant_id)
            serializer = AdminSerializer(merchant, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Merchant.DoesNotExist:
            return Response({"error": "Merchant not found"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, merchant_id):
        """Delete a merchant."""
        try:
            merchant = Merchant.objects.get(merchant_id=merchant_id)
            merchant.delete()
            return Response({"message": "Merchant deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Merchant.DoesNotExist:
            return Response({"error": "Merchant not found"}, status=status.HTTP_404_NOT_FOUND)

#  Admin gets all audit logs
class DashboardAuditLogsView(APIView):
    """Retrieve all admin audit logs."""
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Retrieve admin logs."""
        logs = AuditLog.objects.all()
        serializer = AuditLogSerializer(logs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)