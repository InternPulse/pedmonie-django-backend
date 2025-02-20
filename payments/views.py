from django.shortcuts import render

# Create your views here.
from rest_framework import generics, permissions
from .models import PaymentGateway, MerchantPaymentGateway
from .serializers import PaymentGatewaySerializer, MerchantPaymentGatewaySerializer
from rest_framework_simplejwt.authentication import JWTAuthentication

class PaymentGatewayListView(generics.ListAPIView):
    authentication_classes = JWTAuthentication
    queryset = PaymentGateway.objects.all()
    serializer_class = PaymentGatewaySerializer

class PaymentGatewayDetailView(generics.RetrieveAPIView):
    authentication_classes = JWTAuthentication
    queryset = PaymentGateway.objects.all()
    serializer_class = PaymentGatewaySerializer
    lookup_field = "gateway_id"

class MerchantPaymentGatewayView(generics.RetrieveUpdateAPIView):
    authentication_classes = JWTAuthentication
    queryset = MerchantPaymentGateway.objects.all()
    serializer_class = MerchantPaymentGatewaySerializer
    lookup_field = "gateway_id"
