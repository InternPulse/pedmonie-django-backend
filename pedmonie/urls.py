"""
URL configuration for pedmonie project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
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


    # Explicitly register API paths
    # path("api/v1/admins/", include("dashboard.urls")),
]

