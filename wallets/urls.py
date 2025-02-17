from django.urls import path
from .views import WalletView

urlpatterns = [
    path('api/v1/wallet/', WalletView.as_view(), name='wallet_list'),
    path('api/v1/wallet/<uuid:wallet_id>/', WalletView.as_view(), name='wallet_detail'),
]
