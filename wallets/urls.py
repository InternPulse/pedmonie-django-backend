from django.urls import path
from .views import WalletListView, WalletDetailView


urlpatterns = [
    path('', WalletListView.as_view(), name='wallet-list'),
    path('<str:wallet_id>/', WalletDetailView.as_view(), name='wallet-detail'),
]