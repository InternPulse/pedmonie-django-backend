from django.urls import path
from .views import MerchantCreateView

urlpatterns = [
    path('api/v1/merchants', MerchantCreateView.as_view(), name='create-merchant'),
]