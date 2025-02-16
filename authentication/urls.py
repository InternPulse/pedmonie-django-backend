from django.urls import path
from . import views

urlpatterns = [
    path('api/v1/merchants', views.MerchantCreateView, name='create-merchant'),
]