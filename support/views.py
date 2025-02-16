from django.shortcuts import render

# Create your views here.
from rest_framework import generics, permissions
from .models import SupportTicket, SupportMessage
from .serializers import SupportTicketSerializer, SupportMessageSerializer

class SupportTicketListView(generics.ListCreateAPIView):
    queryset = SupportTicket.objects.all()
    serializer_class = SupportTicketSerializer

class SupportTicketDetailView(generics.RetrieveUpdateAPIView):
    queryset = SupportTicket.objects.all()
    serializer_class = SupportTicketSerializer
    lookup_field = "ticket_id"

class SupportMessageCreateView(generics.CreateAPIView):
    queryset = SupportMessage.objects.all()
    serializer_class = SupportMessageSerializer
