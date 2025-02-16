from django.contrib import admin

# Register your models here.
from .models import SupportTicket, SupportMessage

admin.site.register(SupportTicket)
admin.site.register(SupportMessage)
