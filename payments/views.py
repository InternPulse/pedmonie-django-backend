from django.shortcuts import render

# add authentication to views
from rest_framework.permissions import IsAuthenticated

from rest_framework import generics, permissions
from .models import PaymentGateway, MerchantPaymentGateway
from .serializers import PaymentGatewaySerializer, MerchantPaymentGatewaySerializer

##############################################################################################

# Create your views here.
class PaymentGatewayListView(generics.ListAPIView):
    # ensure the user was authenticated before trying to access the view
    permission_classes = [IsAuthenticated]
    queryset = PaymentGateway.objects.all()
    serializer_class = PaymentGatewaySerializer

class PaymentGatewayDetailView(generics.RetrieveAPIView):
    # ensure the user was authenticated before trying to access the view
    permission_classes = [IsAuthenticated]
    queryset = PaymentGateway.objects.all()
    serializer_class = PaymentGatewaySerializer
    lookup_field = "gateway_id"

class MerchantPaymentGatewayView(generics.RetrieveUpdateAPIView):
    # ensure the user was authenticated before trying to access the view
    permission_classes = [IsAuthenticated]
    queryset = MerchantPaymentGateway.objects.all()
    serializer_class = MerchantPaymentGatewaySerializer
    lookup_field = "gateway_id"
