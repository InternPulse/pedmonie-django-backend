from django.db import models
# wallet/models.py

from django.db import models
from django.contrib.auth import get_user_model

class Wallet(models.Model):
    """Model for storing wallet information for each user."""
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Wallet for {self.user.email} with balance {self.balance}"

