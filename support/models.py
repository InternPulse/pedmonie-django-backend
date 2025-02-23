
from django.db import models
import uuid
from authentication.models import Merchant

# Create your models here.
class SupportTicket(models.Model):
    ticket_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sn = models.CharField(max_length=50,unique=True, db_index=True, verbose_name="Serial Number", blank=True)
    merchant_id = models.ForeignKey(Merchant, on_delete=models.CASCADE, limit_choices_to={'role': 'merchant'}, related_name='support_ticket')
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('resolved', 'Resolved')], default='pending')
    description = models.TextField()
    createdAt = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'support_tickets'
        ordering = ["-createdAt"]

    def _str_(self):
        return f"Ticket {self.ticket_id} - {self.status}"
    
    def save(self, *args, **kwargs):
        if not self.sn:  # Only assign if 'sn' is empty
            last_ticket = SupportTicket.objects.exclude(sn='').order_by(models.functions.Cast('sn', models.IntegerField()).desc()).first()
            if last_ticket and last_ticket.sn.isdigit():
                self.sn = str(int(last_ticket.sn) + 1)
            else:
                self.sn = "1"  # Start from 1 if no records exist
        super().save(*args, **kwargs)
    
   

class SupportMessage(models.Model):
    message_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sn = models.CharField(max_length=50,unique=True, db_index=True, verbose_name="Serial Number", blank=True)
    ticket = models.ForeignKey(SupportTicket, on_delete=models.CASCADE)
    sender = models.ForeignKey(Merchant, on_delete=models.CASCADE)
    message = models.TextField()
    createdAt = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'support_messages'
        ordering = ["-createdAt"]

    def _str_(self):
        return f"Message {self.message_id} on Ticket {self.ticket.ticket_id}"
    def save(self, *args, **kwargs):
        if not self.sn:  # Only assign if 'sn' is empty
            last_message = SupportTicket.objects.exclude(sn='').order_by(models.functions.Cast('sn', models.IntegerField()).desc()).first()
            if last_message and last_message.sn.isdigit():
                self.sn = str(int(last_message.sn) + 1)
            else:
                self.sn = "1"  # Start from 1 if no records exist
        super().save(*args, **kwargs)
