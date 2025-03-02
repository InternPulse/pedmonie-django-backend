"""import admin models from django.contrib"""
from django.contrib import admin
# Register your models here.
from .models import Merchant

#########################################################################

# register Merchant model
# NOTE: don't register MerchantManager
# - it's not a model but a (helper) custom manager class that handles the creation of user instances
# The Django admin site was not displaying the merchant_id
# - add it to the admin interface


@admin.register(Merchant)
class MerchantAdmin(admin.ModelAdmin):
    """This registers the Merchant model to the admin interface"""
    readonly_fields = ('merchant_id',)
