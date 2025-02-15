from django.shortcuts import render

# Create your views here.
from rest_framework import generics, permissions
from .models import PaymentGateway, MerchantPaymentGateway
from .serializers import PaymentGatewaySerializer, MerchantPaymentGatewaySerializer

class PaymentGatewayListView(generics.ListAPIView):
    queryset = PaymentGateway.objects.all()
    serializer_class = PaymentGatewaySerializer

class PaymentGatewayDetailView(generics.RetrieveAPIView):
    queryset = PaymentGateway.objects.all()
    serializer_class = PaymentGatewaySerializer
    lookup_field = "gateway_id"

class MerchantPaymentGatewayView(generics.RetrieveUpdateAPIView):
    queryset = MerchantPaymentGateway.objects.all()
    serializer_class = MerchantPaymentGatewaySerializer
    lookup_field = "gateway_id"
