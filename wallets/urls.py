from django.urls import path
from .views import WalletListView, WalletDetailView, RequestWithdrawalView, MerchantWithdrawalsView, WithdrawalDetailView


urlpatterns = [
    path('admins/wallets/', WalletListView.as_view(), name='wallet-list'),
    path('admins/wallets/<str:wallet_id>/', WalletDetailView.as_view(), name='wallet-detail'),

    # Withdrawals
    path("merchants/<uuid:merchant_id>/withdrawals/", RequestWithdrawalView.as_view(), name="request-withdrawal"),
    path("merchants/<uuid:merchant_id>/withdrawals/all/", MerchantWithdrawalsView.as_view(), name="get-withdrawals"),
    path("merchants/<uuid:merchant_id>/withdrawals/<uuid:withdrawal_id>/", WithdrawalDetailView.as_view(), name="get-withdrawal"),

]

