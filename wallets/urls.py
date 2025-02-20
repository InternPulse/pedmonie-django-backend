from django.urls import path
from .views import WalletListView, WalletDetailView


urlpatterns = [
    path('admins/wallets/', WalletListView.as_view(), name='wallet-list'),
    # path('admins/wallets<str:wallet_id>/', WalletDetailView.as_view(), name='wallet-detail'),
    path("admins/wallets/<uuid:wallet_id>/", WalletDetailView.as_view(), name="wallet-detail"),

]