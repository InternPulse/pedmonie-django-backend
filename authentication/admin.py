from django.contrib import admin

# Register your models here.
from .models import *

#########################################################################

# register Merchant model
# NOTE: don't register MerchantManager
# - it's not a model but a (helper) custom manager class that handles the creation of user instances
admin.site.register(Merchant)
