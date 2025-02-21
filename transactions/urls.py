from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TransactionViewSet

# router = DefaultRouter()
# router.register(r'', TransactionViewSet, basename='transactions')


# router = DefaultRouter()
# router.register(r'transactions', TransactionViewSet, basename='transactions')


router = DefaultRouter()
router.register(r'transactions', TransactionViewSet, basename='transactions')


urlpatterns = [
    path('admins/', include(router.urls)),
    path('admins/transactions_by_wallet/', TransactionViewSet.as_view({'get': 'transactions_by_wallet'}), name='transactions_by_wallet'),
    path('refund_transaction/', TransactionViewSet.as_view({'post': 'refund_transaction'}), name='refund_transaction'),   
]


# from django.urls import path
# from rest_framework.routers import DefaultRouter
# from .views import TransactionViewSet

# router = DefaultRouter()
# router.register(r'', TransactionViewSet, basename='transactions')

# urlpatterns = router.urls
# router = DefaultRouter()
# router.register(r'transactions', TransactionViewSet, basename='transactions')