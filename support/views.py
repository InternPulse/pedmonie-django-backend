from django.shortcuts import render

# add authentication to views
from rest_framework.permissions import IsAuthenticated

from rest_framework import generics, permissions
from .models import SupportTicket, SupportMessage
from .serializers import SupportTicketSerializer, SupportMessageSerializer

# Create your views here.

class SupportTicketListView(generics.ListCreateAPIView):
    # ensure the user was authenticated before trying to access the view
    permission_classes = [IsAuthenticated]
    queryset = SupportTicket.objects.all()
    serializer_class = SupportTicketSerializer

class SupportTicketDetailView(generics.RetrieveUpdateAPIView):
    # ensure the user was authenticated before trying to access the view
    permission_classes = [IsAuthenticated]
    queryset = SupportTicket.objects.all()
    serializer_class = SupportTicketSerializer
    lookup_field = "ticket_id"

class SupportMessageCreateView(generics.CreateAPIView):
    # ensure the user was authenticated before trying to access the view
    permission_classes = [IsAuthenticated]
    queryset = SupportMessage.objects.all()
    serializer_class = SupportMessageSerializer
