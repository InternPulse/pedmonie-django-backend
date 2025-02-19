from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import Wallet
from .serializers import WalletSerializer

# Custom permission class to allow only admins to access wallet endpoints
class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_staff

class WalletListView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsAdminUser]

    def get(self, request,):
        """Get all wallets (admin only)."""
        wallets = Wallet.objects.all()
        serializer = WalletSerializer(wallets, many=True)
        return Response(serializer.data)

class WalletDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsAdminUser]

    def get(self, request, wallet_id):
        """Get a specific wallet by ID (admin only)."""
        wallet = get_object_or_404(Wallet, wallet_id=wallet_id)
        serializer = WalletSerializer(wallet)
        return Response(serializer.data)

    def patch(self, request, wallet_id):
        """Update a specific wallet (admin only)."""
        wallet = get_object_or_404(Wallet, wallet_id=wallet_id)
        serializer = WalletSerializer(wallet, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, wallet_id):
        """Delete a specific wallet (admin only)."""
        wallet = get_object_or_404(Wallet, wallet_id=wallet_id)
        wallet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
