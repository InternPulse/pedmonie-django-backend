from django.urls import path
from .views import PaymentGatewayListView, PaymentGatewayDetailView, MerchantPaymentGatewayView

urlpatterns = [
    path("payment-gateways", PaymentGatewayListView.as_view(), name="list-payment-gateways"),
    path("payment-gateways/<uuid:gateway_id>", PaymentGatewayDetailView.as_view(), name="get-payment-gateway"),
    path("merchants/<uuid:merchant_id>/payment-gateways/<uuid:gateway_id>", MerchantPaymentGatewayView.as_view(), name="get-merchant-payment-gateway"),
]
