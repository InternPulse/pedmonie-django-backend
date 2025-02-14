from django.db import models
import uuid
from django.contrib.auth.models import User

# Audit models here.
class AuditLog(models.Model):
    log_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    admin = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'superadmin'})
    action = models.TextField()  # Example: "Deleted a merchant account"
    created_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"{self.admin.email} - {self.action}"