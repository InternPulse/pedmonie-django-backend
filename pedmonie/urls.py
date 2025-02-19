from django.contrib import admin
from django.urls import path, include

# import built-in views 
# - TokenObtainPairView to handle login with username + password & return access + refresh tokens
# - TokenRefreshView to accept expired refresh token & return new access token
# https://django-rest-framework-simplejwt.readthedocs.io/en/latest/getting_started.html#project-configuration
from rest_framework_simplejwt.views import TokenRefreshView

# import custom view for JWT token generation in athentication app one level up in the directory
from authentication.views import CustomTokenObtainPairView

#########################################################################################################################

# add urls for apps
# add url to login and return JWT access + refresh tokens
# add url to accept expired JWT refresh token & return new JWT token
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('authentication.urls')),
    path('api/v1/', include('dashboard.urls')),
    path("api/v1/", include("payments.urls")),
    path("api/v1/support/", include("support.urls")),   
    path('api/v1/admins/wallets/', include('wallets.urls')),
    path('api/v1/orders/', include('orders.urls')),
    path('api/v1/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
