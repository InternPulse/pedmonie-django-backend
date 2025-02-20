from django.db import models
import uuid
from authentication.models import Merchant

# Create your models here.
class SupportTicket(models.Model):
    ticket_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sn = models.CharField(max_length=50,unique=True, db_index=True, verbose_name="Serial Number", blank=True)
    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE, limit_choices_to={'role': 'merchant'})
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('resolved', 'Resolved')], default='pending')
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"Ticket {self.ticket_id} - {self.status}"
    def save(self, *args, **kwargs):
        if not self.sn:  # Only assign if 'sn' is empty
            last_ST = SupportTicket.objects.order_by('-sn').first()
            if last_ST and last_ST.sn.isdigit():
                self.sn = str(int(last_ST.sn) + 1)
            else:
                self.sn = "1"  # Start from 1 if no records exist
        super().save(*args, **kwargs)

class SupportMessage(models.Model):
    message_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ticket = models.ForeignKey(SupportTicket, on_delete=models.CASCADE)
    sender = models.ForeignKey(Merchant, on_delete=models.CASCADE)
    message = models.TextField()
    createdAt = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"Message {self.message_id} on Ticket {self.ticket.ticket_id}"
    def save(self, *args, **kwargs):
        if not self.sn:  # Only assign if 'sn' is empty
            last_sn = SupportMessage.objects.order_by('-message_id').first()
            if last_sn and last_sn.sn.isdigit():
                self.sn = str(int(last_sn.sn) + 1)
            else:
                self.sn = "1"  # Start from 1 if no records exist
        super().save(*args, **kwargs)

    def __str__(self):
        return self.sn