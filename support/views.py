from django.shortcuts import render

# Create your views here.
from rest_framework import generics, permissions
from .models import SupportTicket, SupportMessage
from .serializers import SupportTicketSerializer, SupportMessageSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication

class SupportTicketListView(generics.ListCreateAPIView):
    authentication_classes = JWTAuthentication
    queryset = SupportTicket.objects.all()
    serializer_class = SupportTicketSerializer

class SupportTicketDetailView(generics.RetrieveUpdateAPIView):
    authentication_classes = JWTAuthentication
    queryset = SupportTicket.objects.all()
    serializer_class = SupportTicketSerializer
    lookup_field = "ticket_id"

class SupportMessageCreateView(generics.CreateAPIView):
    authentication_classes = JWTAuthentication
    queryset = SupportMessage.objects.all()
    serializer_class = SupportMessageSerializer
