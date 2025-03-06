from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import OrderViewSet
router = DefaultRouter()
router.register(r'orders', OrderViewSet, basename='order')

urlpatterns = [
    path('admins/', include(router.urls)),

]
