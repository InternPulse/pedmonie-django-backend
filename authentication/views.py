from django.shortcuts import render

# API view allows for message customisation without overriding methods
# using it since there are 2 endpoints: create, retrieve
from rest_framework.views import APIView

# handle API responses with proper formatting
from rest_framework.response import Response

# provide permission classes & HTTP status codes for API endpoints
# https://www.django-rest-framework.org/tutorial/3-class-based-views/#using-generic-class-based-views
from rest_framework import permissions, status, viewsets

# use JWT token-based authentication
from rest_framework_simplejwt.authentication import JWTAuthentication

# import Merchant model from the current directory
from .models import Merchant

# import serializer for superuser (Admin) user operations
from .serializers import AdminSerializer, MerchantRegistrationSerializer, MerchantProfileSerializer, MerchantLoginSerializer, VerifyEmailSerializer

# import Django's exception for handling objects that do not exist
from django.core.exceptions import ObjectDoesNotExist 

# import JWT token view to generate a token
from rest_framework_simplejwt.views import TokenObtainPairView

# import custom serializer for a custom view to obtain a token 
from .serializers import CustomTokenObtainPairSerializer


from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny

###############################################################################################################

# create a custom view that inherits from DRF's built-in token view to generate a JWT token with custom claims
# - uses custom serializer for email-based authentication & add custom custom claims 
# keep the custom JWT setting local to the auth app, instead of doing it in settings.py making it global
# https://django-rest-framework-simplejwt.readthedocs.io/en/latest/customizing_token_claims.html#customizing-token-claims
class CustomTokenObtainPairView(TokenObtainPairView):
    # specify the custom serializer class that defines token customisations
    serializer_class = CustomTokenObtainPairSerializer

# a class to create & retrieve superusers
class AdminView(APIView):
    # set JWT as the authentication method for this view (needs a valid token in request header)
    authentication_classes = [JWTAuthentication]
    # check that the user was authenticated with is_staff=True with Django REST Framework's built-in permission class(IsAdminUser)
    # don't add IsAuthenticated as IsAdminUser already inherits from IsAuthenticated
    permission_classes = [permissions.IsAdminUser]

    # a method to carry out superuser creation
    def post(self, request):
        """Handle the POST request to create a new superuser.

        :param request: HTTP request containing admin data
        :type request: rest_framework.request.Request
        :return: Response with created superuser data or error message
        :rtype: rest_framework.response.Response
        """
        # create an instance of AdminSerializer with the data from the HTTP POST request
        serializer = AdminSerializer(data=request.data)

        # check if the submitted data passes all validation rules defined in serializer
        if serializer.is_valid():
            # save the superuser
            # ensure only superadmins get created
            serializer.save(role='superadmin', is_staff=True, is_superuser=True)

            # return a response with a message if the Superadmin was created        
            return Response(
                {
                    "status": "success",
                    "code": 201,
                    "message": "Successfully added a Superadmin",
                    "data": serializer.data,                
                },            
                status=status.HTTP_201_CREATED,             
                )    
        
        # return a response with an unsuccessful message if the Superadmin was not created        
        return Response(
            {
                "status": "error",
                "code": 400,
                "message": "Unsuccessful creating a Superadmin with invalid data",    
                "errors": serializer.errors,            
                "data": serializer.data,                
            },            
            status=status.HTTP_400_BAD_REQUEST,             
            )
    
    # a method to retrieve a Superadmin
    def get(self, request, merchant_id=None):
        """Retrieve a Superadmin by their merchant_id.

        :param request: HTTP request object
        :type request: rest_framework.request.Request
        :param merchant_id: Unique identifier for merchant, defaults to None
        :type merchant_id: str, optional
        :return: Response with superuser data or error message
        :rtype: rest_framework.response.Response
        """
        # use defensive programming with try-except blocks to retrieve a superuser
        try:
            # get the superadmin object
            # if the superadmin does not exist, return a 404 error
            superadmin = Merchant.objects.get(merchant_id=merchant_id, is_superuser=True)

            # serialize the superadmin object
            serializer = AdminSerializer(superadmin)

            # return a response with the serialized data
            return Response(
                {
                    "status": "success",
                    "code": 200,
                    "message": f"Successfully retrieved the Superadmin merchant with ID: {merchant_id}.",
                    "data": serializer.data,
                },
                status=status.HTTP_200_OK,
                )
        
        except ObjectDoesNotExist:
            # return a response with a message if the Superadmin does not exist
            return Response(
                {
                    "status": "error",
                    "code": 404,
                    "message": "A Superadmin with this merchant ID does not exist.",
                    "data": None,
                },
                status=status.HTTP_404_NOT_FOUND,
                )

