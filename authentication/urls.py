from django.urls import path
from .views import MerchantCreateView, MerchantLoginView, MerchantLogoutView

urlpatterns = [
    path("api/v1/merchants/", MerchantCreateView.as_view(), name="create-merchant"),
    path("api/v1/auth/merchants/signin/", MerchantLoginView.as_view(), name="merchant-login"),
    path("api/v1/auth/merchants/logout/", MerchantLogoutView.as_view(), name="merchant-logout"),
]
