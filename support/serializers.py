from rest_framework import serializers
from .models import SupportTicket, SupportMessage

class SupportTicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupportTicket
        fields = '__all__'

class SupportMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = SupportMessage
        fields = '__all__'
