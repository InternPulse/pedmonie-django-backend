from django.shortcuts import render

from rest_framework import generics
from .models import Merchant
from .serializers import MerchantSerializer

class MerchantCreateView(generics.CreateAPIView):
    queryset = Merchant.objects.all()
    serializer_class = MerchantSerializer
