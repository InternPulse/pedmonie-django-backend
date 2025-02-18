from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/v1/", include("authentication.urls")),  # Authentication Endpoints
    path("api/v1/", include("dashboard.urls")),       # Dashboard Endpoints
    path("api/v1/", include("payments.urls")),        # Payment Endpoints
    path("api/v1/", include("support.urls")),         # Support Endpoints
    path("api/v1/", include("wallets.urls")),         # Wallet Endpoints
    path("api/v1/", include("orders.urls")),          # Order Endpoints

]

