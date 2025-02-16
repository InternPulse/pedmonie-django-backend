# import path for URL pattern routing in Django
from django.urls import path

# import AdminView class from views.py in the current directory
from .views import AdminView

########################################################################################################################

# add url to superuser post method
# add url to superuser get method
# don't specify method -> APIView automatically maps HTTP methods (POST, GET) to corresponding class methods with as_view()
urlpatterns = [
    path('api/v1/admins/', AdminView.as_view(), name='create_superuser'), 
    path('api/v1/admins/<uuid:merchant_id>/', AdminView.as_view(), name='get_superuser'),    
]