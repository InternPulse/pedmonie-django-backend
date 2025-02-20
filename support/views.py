from django.shortcuts import render

# add authentication to views
from rest_framework.permissions import IsAuthenticated

from rest_framework import generics, permissions, status
from .models import SupportTicket, SupportMessage
from .serializers import SupportTicketSerializer, SupportMessageSerializer, CreateSupportTicketSerializer
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

# Create your views here.

class SupportTicketListView(generics.ListCreateAPIView):
  # ensure the user was authenticated before trying to access the view

    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff: 
            return SupportTicket.objects.all()
        return SupportTicket.objects.filter(merchant=user)

    def get_serializer_class(self):
        user = self.request.user
        if user.is_staff:
            return SupportTicketSerializer
        return CreateSupportTicketSerializer

    def create(self, request, *args, **kwargs):
        # if request.user.is_staff:
        #     return Response(
        #         {"detail": "Admins are not allowed to create support tickets."},
        #         status=status.HTTP_403_FORBIDDEN,
        #     )
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(merchant=self.request.user, status="pending")

class SupportTicketDetailView(generics.RetrieveUpdateAPIView):
    # ensure the user was authenticated before trying to access the view
    permission_classes = [IsAuthenticated]
    queryset = SupportTicket.objects.all()
    serializer_class = SupportTicketSerializer
    lookup_field = "ticket_id"

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return SupportTicket.objects.all()  
        return SupportTicket.objects.filter(merchant=user)

    def update(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return Response(
                {"detail": "Only admins can update support tickets."},
                status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)


class SupportMessageCreateView(generics.CreateAPIView):
    # ensure the user was authenticated before trying to access the view
    permission_classes = [IsAuthenticated]
    queryset = SupportMessage.objects.all()
    serializer_class = SupportMessageSerializer

    def create(self, request, *args, **kwargs):
        ticket_id = kwargs.get("ticket_id")
        ticket = get_object_or_404(SupportTicket, ticket_id=ticket_id)
        user = request.user
        if not user.is_staff and ticket.merchant != user:
            return Response(
                {"detail": "You can only send messages to your own support tickets."},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(ticket=ticket, sender=user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)