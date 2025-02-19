from django.db import models
import uuid
from authentication.models import Merchant  

class AuditLog(models.Model):
    log_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    admin = models.ForeignKey(Merchant, on_delete=models.CASCADE, limit_choices_to={'role': 'superadmin'})  # Reference Merchant model
    action = models.TextField()  # Example: "Deleted a merchant account"
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.admin.email} - {self.action}"
