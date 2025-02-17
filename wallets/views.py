from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Wallet
from .serializers import WalletSerializer

# Restrict access to admins only
class IsAdminUser(permissions.BasePermission):
    """Custom permission to allow only admins to access wallet endpoints"""
    def has_permission(self, request, view):
        return request.user and request.user.is_superuser

class WalletView(generics.GenericAPIView):
    """Handles listing, retrieving, updating, and deleting wallets (Admin Only)"""
    serializer_class = WalletSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        """Retrieve all wallets (Admins only)"""
        return Wallet.objects.all()

    def get(self, request, wallet_id=None):
        """Retrieve all wallets or a specific wallet"""
        if wallet_id:
            wallet = get_object_or_404(Wallet, id=wallet_id)
            serializer = self.get_serializer(wallet)
        else:
            wallets = self.get_queryset()
            serializer = self.get_serializer(wallets, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, wallet_id):
        """Update wallet details (Admins only)"""
        wallet = get_object_or_404(Wallet, id=wallet_id)
        serializer = self.get_serializer(wallet, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, wallet_id):
        """Delete a wallet (Admins only)"""
        wallet = get_object_or_404(Wallet, id=wallet_id)
        wallet.delete()
        return Response({"message": "Wallet deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
