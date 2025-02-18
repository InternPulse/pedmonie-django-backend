from rest_framework.routers import DefaultRouter
from .views import OrderViewSet
from django.urls import path, include

router = DefaultRouter()
router.register(r'orders', OrderViewSet, basename='order')

urlpatterns = [
    path('', include(router.urls)),
]