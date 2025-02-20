from django.shortcuts import render

from rest_framework import viewsets,permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from transactions.models import Transaction
from .serializers import TransactionSerializer
class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_staff
class TransactionViewSet(viewsets.ViewSet):
    permission_classes = [IsAdminUser]
    def list(self, request):
        transactions = Transaction.objects.all()
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)
    def retrieve(self, request, pk=None):
        try:
            transaction = Transaction.objects.get(transaction_id=pk)
            serializer = TransactionSerializer(transaction)
            return Response(serializer.data)
        except Transaction.DoesNotExist:
            return Response({"error": "Transaction not found"}, status=status.HTTP_404_NOT_FOUND)
    @action(detail=False, methods=["get"], url_path="wallets/(?P<wallet_id>[^/.]+)/transactions")
    def transactions_by_wallet(self, request, wallet_id=None):
        transactions = Transaction.objects.filter(order_id=wallet_id)
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)
    @action(detail=True, methods=["post"], url_path="refund")
    def refund_transaction(self, request, pk=None):
        try:
            transaction = Transaction.objects.get(transaction_id=pk)
            if transaction.status != "successful":
                return Response({"error": "Only successful transactions can be refunded"}, status=status.HTTP_400_BAD_REQUEST)
            transaction.status = "pending"  # Simulating refund processing
            transaction.save()
            return Response({"message": "Transaction refund initiated"}, status=status.HTTP_200_OK)
        except Transaction.DoesNotExist:
            return Response({"error": "Transaction not found"}, status=status.HTTP_404_NOT_FOUND)
