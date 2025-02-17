from django.urls import path, include
from .views import MerchantViewSet
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

router = DefaultRouter()
router.register(r'merchants', MerchantViewSet, basename='merchant')


urlpatterns = [
    path('', include(router.urls)),
    path('auth/verify-email/', MerchantViewSet.as_view({'post': 'verify_email'}), name='verify-email'),
    path('auth/merchant/signin/', MerchantViewSet.as_view({'post': 'signin'}), name='merchant-signin'),
    path('token/refresh', TokenRefreshView.as_view(), name='token-refresh'),
    path('merchants/<uuid:merchant_id>/', MerchantViewSet.as_view({'get': 'retrieve'}))
]