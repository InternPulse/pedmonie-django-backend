from django.urls import path
from .views import RequestWithdrawal, MerchantWithdrawalsList, GetWithdrawalDetail

urlpatterns = [
    path('merchants/<str:merchant_id>/withdrawals', RequestWithdrawal.as_view(), name='request-withdrawal'),
    path('merchants/<str:merchant_id>/withdrawals', MerchantWithdrawalsList.as_view(), name='merchant-withdrawals-list'),
    path('merchants/<str:merchant_id>/withdrawals/<int:withdrawal_id>', GetWithdrawalDetail.as_view(), name='withdrawal-detail'),
]
