from django.urls import path
from .views import (
    MerchantListView, MerchantDetailView, MerchantUpdateView,
    MerchantDeleteView, AuditLogListView
)

urlpatterns = [
    path("admins/merchants/", MerchantListView.as_view(), name="list-merchants"),
    path("admins/merchants/<uuid:merchant_id>/", MerchantDetailView.as_view(), name="get-merchant"),
    path("admins/merchants/<uuid:merchant_id>/update/", MerchantUpdateView.as_view(), name="update-merchant"),
    path("admins/merchants/<uuid:merchant_id>/delete/", MerchantDeleteView.as_view(), name="delete-merchant"),
    path("admins/logs/", AuditLogListView.as_view(), name="admin-logs"),
]
