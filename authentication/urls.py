from django.urls import path
from .views import AdminRegistrationView, MerchantRegistrationView, MerchantLoginView, VerifyOTPView

urlpatterns = [
    # Admin Authentication
    path("auth/admins/", AdminRegistrationView.as_view(), name="admin-register"),

    # Merchant Authentication
    path("auth/merchants/", MerchantRegistrationView.as_view(), name="merchant-register"),
    path("auth/merchants/verify-otp/", VerifyOTPView.as_view(), name="verify-otp"),
    path("auth/merchants/signin/", MerchantLoginView.as_view(), name="merchant-login"),
]
