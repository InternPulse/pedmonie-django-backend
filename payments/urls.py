from django.urls import path
from .views import (
    PaymentGatewayListView,
    PaymentGatewayDetailView,
    AdminPaymentGatewayCreateView,
    AdminPaymentGatewayUpdateView,
    MerchantPaymentGatewayView,
)

urlpatterns = [
    # Public Payment Gateway Routes
    path("payment-gateways/", PaymentGatewayListView.as_view(), name="list-payment-gateways"),
    path("payment-gateways/<uuid:gateway_id>/", PaymentGatewayDetailView.as_view(), name="get-payment-gateway"),

    # Admin Payment Gateway Management
    path("admins/payment-gateways/", AdminPaymentGatewayCreateView.as_view(), name="add-payment-gateway"),
    path("admins/payment-gateways/<uuid:gateway_id>/", AdminPaymentGatewayUpdateView.as_view(), name="update-payment-gateway"),

    # Merchant Payment Gateway Management
    path("merchants/<uuid:merchant_id>/payment-gateways/", MerchantPaymentGatewayView.as_view(), name="get-merchant-payment-gateway"),
    path("merchants/<uuid:merchant_id>/payments/<uuid:gateway_id>/", MerchantPaymentGatewayView.as_view(), name="update-merchant-payment-gateway"),
]
