# import path for URL pattern routing in Django
from django.urls import path, include

# import AdminView class from views.py in the current directory
from .views import AdminView, MerchantViewSet

from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView


########################################################################################################################

# add url to superuser post method
# add url to superuser get method
# don't specify method -> APIView automatically maps HTTP methods (POST, GET) to corresponding class methods with as_view()


router = DefaultRouter()
router.register(r'merchants', MerchantViewSet, basename='merchant')


urlpatterns = [
    path('', include(router.urls)),
    path('admins/', AdminView.as_view(), name='create_superuser'), 
    path('admins/<uuid:merchant_id>/', AdminView.as_view(), name='get_superuser'),
    path('verify-email/', MerchantViewSet.as_view({'post': 'verify_email'}), name='verify-email'),
    path('signin/', MerchantViewSet.as_view({'post': 'signin'}), name='merchant-signin'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('merchants/<uuid:merchant_id>/', MerchantViewSet.as_view({'get': 'retrieve'}))
    
]