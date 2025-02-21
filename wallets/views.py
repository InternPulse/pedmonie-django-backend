from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import Wallet, Withdrawal
from authentication.models import Merchant
from .serializers import WalletSerializer, WithdrawalSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication


# Custom permission class to allow only admins to access wallet endpoints
class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_staff

class WalletListView(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated, IsAdminUser]

    def get(self, request,):
        """Get all wallets (admin only)."""
        wallets = Wallet.objects.all()
        serializer = WalletSerializer(wallets, many=True)
        return Response(serializer.data)

class WalletDetailView(APIView):

    authentication_classes = [JWTAuthentication]
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


class RequestWithdrawalView(APIView):
    """Allow merchants to request a withdrawal"""

    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, merchant_id):
        merchant = get_object_or_404(Merchant, merchant_id=merchant_id)

        # Ensure the requesting user is the owner of the wallet
        if request.user != merchant:
            return Response({"error": "You are not authorized to withdraw from this wallet."}, status=status.HTTP_403_FORBIDDEN)

        serializer = WithdrawalSerializer(data=request.data, context={'merchant': merchant})
        if serializer.is_valid():
            # Deduct amount from wallet balance
            wallet = Wallet.objects.filter(merchant=merchant).first()
            withdrawal_amount = serializer.validated_data['amount']
            initial_balance = wallet.amount
            final_balance = initial_balance - withdrawal_amount

            # Create withdrawal record
            withdrawal = Withdrawal.objects.create(
                merchant=merchant,
                amount=withdrawal_amount,
                initial_balance=initial_balance,
                final_balance=final_balance,
                status="pending"
            )

            # Deduct amount from wallet
            wallet.amount = final_balance
            wallet.save()

            return Response({
                "message": "Withdrawal request submitted successfully.",
                "sn": withdrawal.sn,  # Include SN
                "withdrawal_id": withdrawal.withdrawal_id,
                "initial_balance": initial_balance,
                "final_balance": final_balance,
                "status": withdrawal.status
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MerchantWithdrawalsView(APIView):
    """Get all withdrawals for a specific merchant"""

    authentication_classes = [JWTAuthentication]
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, merchant_id):
        merchant = get_object_or_404(Merchant, merchant_id=merchant_id)

        # Ensure only the merchant can view their withdrawals
        if request.user != merchant:
            return Response({"error": "Unauthorized access."}, status=status.HTTP_403_FORBIDDEN)

        withdrawals = Withdrawal.objects.filter(merchant=merchant)
        serializer = WithdrawalSerializer(withdrawals, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class WithdrawalDetailView(APIView):
    """Get details of a specific withdrawal"""
    
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, merchant_id, withdrawal_id):
        merchant = get_object_or_404(Merchant, merchant_id=merchant_id)

        # Ensure only the merchant can view this withdrawal
        if request.user != merchant:
            return Response({"error": "Unauthorized access."}, status=status.HTTP_403_FORBIDDEN)

        withdrawal = get_object_or_404(Withdrawal, withdrawal_id=withdrawal_id, merchant=merchant)
        serializer = WithdrawalSerializer(withdrawal)
        return Response(serializer.data, status=status.HTTP_200_OK)

