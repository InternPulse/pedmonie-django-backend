from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.shortcuts import get_object_or_404
from authentication.models import Merchant
from .models import PaymentGateway, MerchantPaymentGateway
from .serializers import PaymentGatewaySerializer, MerchantPaymentGatewaySerializer
from rest_framework.permissions import IsAuthenticated


class PaymentGatewayListView(APIView):
    """
    Retrieve all available payment gateways (Public Access)
    """

    permission_classes = [permissions.AllowAny]

    def get(self, request):
        gateways = PaymentGateway.objects.all()
        serializer = PaymentGatewaySerializer(gateways, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PaymentGatewayDetailView(APIView):
    """
    Retrieve a single payment gateway by ID
    """

    permission_classes = [permissions.AllowAny]

    def get(self, request, gateway_id):
        gateway = get_object_or_404(PaymentGateway, gateway_id=gateway_id)
        serializer = PaymentGatewaySerializer(gateway)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AdminPaymentGatewayCreateView(APIView):
    """
    Admin: Add a new payment gateway
    """

    permission_classes = [permissions.IsAdminUser]

    def post(self, request):
        serializer = PaymentGatewaySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Payment gateway added successfully", "data": serializer.data},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdminPaymentGatewayUpdateView(APIView):
    """
    Admin: Update an existing payment gateway
    """

    permission_classes = [permissions.IsAdminUser]

    def patch(self, request, gateway_id):
        gateway = get_object_or_404(PaymentGateway, gateway_id=gateway_id)
        serializer = PaymentGatewaySerializer(gateway, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Payment gateway updated successfully", "data": serializer.data},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MerchantPaymentGatewayView(APIView):
    """
    Retrieve or update a merchant's enabled payment gateways
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, merchant_id):
        merchant = get_object_or_404(Merchant, merchant_id=merchant_id)
        merchant_gateways = get_object_or_404(MerchantPaymentGateway, merchant=merchant)

        return Response(
            {
                "merchant_id": str(merchant.merchant_id),
                "payment_gateways": merchant_gateways.payment_gateways,
            },
            status=status.HTTP_200_OK,
        )

    def patch(self, request, merchant_id, gateway_id):
        """Enable or disable a specific payment gateway for a merchant"""
        merchant = get_object_or_404(Merchant, merchant_id=merchant_id)
        merchant_gateways, created = MerchantPaymentGateway.objects.get_or_create(merchant=merchant)

        # Get the requested gateway settings
        new_gateways = merchant_gateways.payment_gateways

        if gateway_id not in new_gateways:
            return Response(
                {"error": "Payment gateway not found for this merchant"},
                status=status.HTTP_404_NOT_FOUND,
            )

        # Toggle activation status
        new_gateways[gateway_id]["enabled"] = not new_gateways[gateway_id]["enabled"]
        merchant_gateways.payment_gateways = new_gateways
        merchant_gateways.save()

        return Response(
            {"message": "Payment gateway status updated", "payment_gateways": new_gateways},
            status=status.HTTP_200_OK,
        )
