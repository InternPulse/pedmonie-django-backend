from django.db import models

from django.db import models
import uuid

class Merchant(models.Model):
    merchant_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    surname = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    business_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    is_email_verified = models.BooleanField(default=False)
    password_hash = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    role = models.CharField(max_length=20, choices=[('merchant', 'Merchant'), ('superadmin', 'SuperAdmin')], default='merchant')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)