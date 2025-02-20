from django.db import models
import uuid
from authentication.models import Merchant  

class AuditLog(models.Model):
    log_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sn = models.CharField(max_length=50,unique=True, db_index=True, verbose_name="Serial Number", blank=True)
    admin = models.ForeignKey(Merchant, on_delete=models.CASCADE, limit_choices_to={'role': 'superadmin'})  # Reference Merchant model
    action = models.TextField()  # Example: "Deleted a merchant account"
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.admin.email} - {self.action}"
    
    def save(self, *args, **kwargs):
        if not self.sn:  # Only assign if 'sn' is empty
            last_sn = AuditLog.objects.order_by('-log_id').first()
            if last_sn and last_sn.sn.isdigit():
                self.sn = str(int(last_sn.sn) + 1)
            else:
                self.sn = "1"  # Start from 1 if no records exist
        super().save(*args, **kwargs)

    def __str__(self):
        return self.sn
