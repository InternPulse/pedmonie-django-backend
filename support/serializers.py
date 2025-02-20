from rest_framework import serializers
from .models import SupportTicket, SupportMessage

# class SupportTicketSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = SupportTicket
#         fields = '__all__'

# class SupportMessageSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = SupportMessage
#         fields = '__all__'

class SupportMessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.CharField(source='sender.name', read_only=True)

    class Meta:
        model = SupportMessage
        fields = ['message_id', 'ticket', 'sender', 'sender_name', 'message', 'createdAt']
        read_only_fields = ['message_id', 'createdAt']

class SupportTicketSerializer(serializers.ModelSerializer):
    messages = SupportMessageSerializer(many=True, read_only=True, source='supportmessage_set')
    merchant_name = serializers.CharField(source='merchant.name', read_only=True)


