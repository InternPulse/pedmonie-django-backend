from django.shortcuts import get_object_or_404
import hashlib
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework import serializers
from .utils import generate_verification_token, store_verification_token, send_verification_email, verify_token, store_merchant_data, clear_merchant_data, get_merchant_data
import uuid
from wallets.models import Wallet
from django.db import transaction
import logging


logger = logging.getLogger(__name__)

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
                    "status": "True",
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
                    "status": "False",
                    "code": 404,
                    "message": "A Superadmin with this merchant ID does not exist.",
                    "data": None,
                },
                status=status.HTTP_404_NOT_FOUND,
                )



class MerchantViewSet(viewsets.ModelViewSet):
    """
    Viewset for handling all merchant operations including, registration, 
     email verification, authentication, and profile retrival 
    """

    # authentication_classes = [JWTAuthentication]
    queryset = Merchant.objects.all()       #Fetch all merchants from the database.
    lookup_field = 'merchant_id'            #Use 'merchant_id' instead of the default primary key for lookups

    def get_authentication_classes(self):
        """
        Return the appropriate authentication class based on the requested action.
        """

        if self.action in ['signin', 'verify_email']:
            return []  #No authentication needed
        return [JWTAuthentication]      #Default authentication for other actions
        


    def get_serializer_class(self):
        """
        Return appropriate serializer class based on the requested action.
        """
        if self.action == 'create':
            return MerchantRegistrationSerializer
        elif self.action == 'verify_email':
            return VerifyEmailSerializer
        elif self.action == 'signin':
            return MerchantLoginSerializer
        return MerchantProfileSerializer
    def get_permissions(self):
        """
        Return appropriate permission class based on the requested action.
        - Allow any user to create an account, verify email, or sign in.
        - Require authentication for all other actions.
        """
        if self.action in ['create', 'verify_email', 'signin']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    

    





    

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            token = generate_verification_token()

            merchant_data = serializer.validated_data
            merchant_data.pop('confirm_password', None)
            merchant_data = {k: str(v) for k, v in merchant_data.items()}

            logger.info(f"Merchant data: {merchant_data}")

            if store_merchant_data(merchant_data['email'], merchant_data):
                logger.info(f"Merchant data stored successfully.")
            
                if store_verification_token(merchant_data['email'], token):
                    logger.info(f"Verification token stored successfully.")
                
                    if send_verification_email(merchant_data['email'], token):
                        logger.info(f"Verification email sent.")
                        return Response({
                            'status': 'True',
                            'message': 'Pedmonie verification email sent. Please check your email to complete registration'
                        }, status=status.HTTP_200_OK)
                    else:
                        logger.error(f"Failed to send verification email.")
                        return Response({
                            'status': 'False',
                            'message': 'Failed to send verification email.'
                        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                else:
                    logger.error(f"Failed to store verification token.")
                    return Response({
                        'status': 'False',
                        'message': 'Failed to process registration.'
                    }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                logger.error(f"Failed to store merchant data.")
                return Response({
                    'status': 'False',
                    'message': 'Registration data validation failed.'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            logger.error(f"Invalid serializer data: {serializer.errors}")
            return Response({
                'status': 'False',
                'message': 'Invalid registration data.'
            }, status=status.HTTP_400_BAD_REQUEST)

    


    @action(detail=False, methods=['POST'])
    def verify_email(self, request):
        email = request.data.get('email')
        token = request.data.get('token')

        if not email or not token:
            return Response({
                'status': 'False',
                'message': 'Email and token are required'
            }, status=status.HTTP_400_BAD_REQUEST)
        if verify_token(email, token):
            merchant_data = get_merchant_data(email)
            if not merchant_data:
                return Response({
                    'status': 'False',
                    'message': 'Registration data expired or not found'
                }, status=status.HTTP_400_BAD_REQUEST)
        
            try:
                with transaction.atomic():

                    password = merchant_data.pop('password')
                    merchant = Merchant.objects.create_user(
                        password=password,
                        is_email_verified=True,
                        **merchant_data
                    )

                    wallet = Wallet.objects.create(
                        merchant=merchant,
                        amount=0.0,
                        currency='NGN'

                    )
                    clear_merchant_data(email)

                    refresh = RefreshToken.for_user(merchant)

                    return Response({
                        'status': 'True',
                        'message': 'Email verified and account created successfully.',
                        'data': {
                            'merchant_id': merchant.merchant_id,
                            'email': merchant.email,
                            'business_name': merchant.business_name,
                            'wallet_id': wallet.wallet_id,
                            'access_token': str(refresh.access_token),
                            'refresh_token': str(refresh)
                        }
                    }, status=status.HTTP_201_CREATED)
            except Exception as e:
                logger.error(f'Error creating merchant account {str(e)}')
                return Response({
                    'status': 'False',
                    'message': 'Failed to create account'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({
            'status': False,
            'message':'Invalid or expired verification token',
        }, status=status.HTTP_400_BAD_REQUEST)
    
    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve merchant's  profile details 
        """
        instance = self.get_object()

        #Check if the requesting user is the profile owner
        if not request.user.is_authenticated or request.user.merchant_id != instance.merchant_id:
            return Response({
                'status': 'False',
                'message': 'Access denied: You do not have permission to view this profile'
            }, status=status.HTTP_403_FORBIDDEN)
        if not instance.is_email_verified:
            return Response({
                'status': 'False',
                'message': 'Please verify your email before accessing your profile'
            }, status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(instance)
        return Response({
            'status': 'True',
            'message': 'Merchant profile retrieved successfully',
            'data': serializer.data
        }, status=status.HTTP_200_OK)
    
    def get_object(self):
        """
        Override to lookup merchant by merchant_id instead of the default primary key.
        """
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        merchant_id = self.kwargs.get(lookup_url_kwarg or self.lookup_field)
        if not merchant_id:
            raise serializers.ValidationError('Merchant ID is required')
        merchant = get_object_or_404(Merchant, merchant_id=merchant_id)
        # return get_object_or_404(Merchant, merchant_id=merchant_id)
        self.check_object_permissions(self.request, merchant)
        return merchant
      















