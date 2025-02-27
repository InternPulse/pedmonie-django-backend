
from django.db import models
import uuid
from authentication.models import Merchant

# Create your models here.
class SupportTicket(models.Model):
    ticket_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sn = models.IntegerField(unique=True, db_index=True, verbose_name="Serial Number")
    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE, limit_choices_to={'role': 'merchant'}, related_name='support_ticket')
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('resolved', 'Resolved')], default='pending')
    description = models.TextField()
    createdAt = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'support_tickets'
        ordering = ["-createdAt"]

    def save(self, *args, **kwargs):
        if not self.sn:  # Only assign if 'sn' is empty
            last_sn = SupportTicket.objects.order_by('-sn').first()
            self.sn = last_sn.sn + 1 if last_sn else 1
        super().save(*args, **kwargs)

    def _str_(self):
        return f"Ticket {self.ticket_id} - {self.status}"
    
    
   

class SupportMessage(models.Model):
    message_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sn = models.IntegerField(unique=True, db_index=True, verbose_name="Serial Number")
    ticket = models.ForeignKey(SupportTicket, on_delete=models.CASCADE)
    sender = models.ForeignKey(Merchant, on_delete=models.CASCADE)
    message = models.TextField()
    createdAt = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'support_messages'
        ordering = ["-createdAt"]

    def save(self, *args, **kwargs):
        if not self.sn:  # Only assign if 'sn' is empty
            last_sn = SupportMessage.objects.order_by('-sn').first()
            self.sn = last_sn.sn + 1 if last_sn else 1
        super().save(*args, **kwargs)

    def _str_(self):
        return f"Message {self.message_id} on Ticket {self.ticket.ticket_id}"
    
