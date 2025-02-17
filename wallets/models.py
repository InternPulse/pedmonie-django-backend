from django.db import models

# Create your models here.
# import serializers to convert complex datatypes like django model to pyhton datatypes that can be easily rendered in JSON, XML, etc
# from rest_framework import serializers


# from authentication.models import Merchant
# import uuid


# class WalletSerializer(serializers.ModelSerializer):
#     currency = serializers.CharField(default="€", read_only=True)

#     class Meta:
#         model = Merchant  
#         fields = ['total_balance', 'currency', 'created_at', 'updated_at']
#         read_only_fields = ['created_at', 'updated_at']

#         def get_wallet_id(self, obj):
#             return str(uuid.uuid4())
        