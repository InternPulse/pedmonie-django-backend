from django.db import models
import uuid
from authentication.models import Merchant  

class AuditLog(models.Model):
    log_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sn = models.AutoField(unique=True, db_index=True, verbose_name="Serial Number")
    admin = models.ForeignKey(Merchant, on_delete=models.CASCADE, limit_choices_to={'role': 'superadmin'})  # Reference Merchant model
    action = models.TextField()  # Example: "Deleted a merchant account"
    createdAt = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'auditlog'

    
    def __str__(self):
        return f"{self.admin.email} - {self.action}"
