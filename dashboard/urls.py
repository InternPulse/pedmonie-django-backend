from django.urls import path
from .views import MerchantListView, MerchantDetailView, DashboardAuditLogsView

urlpatterns = [
    # Admin Merchant Management
    path("admins/merchants/", MerchantListView.as_view(), name="list-merchants"),
    path("admins/merchants/<uuid:merchant_id>/", MerchantDetailView.as_view(), name="get-merchant"),

    # Admin Logs
    path("admins/logs/", DashboardAuditLogsView.as_view(), name="admin-logs"),
]
