
from rest_framework import viewsets, status,permissions
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404
import hashlib
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework import serializers
from .utils import generate_verification_token, store_verification_token, send_verification_email, verify_token

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



class MerchantViewSet(viewsets.ModelViewSet):
    """
    Viewset for handling all merchant operations including, registration, 
     email verification, authentication, and profile retrival 
    """

    queryset = Merchant.objects.all()       #Fetch all merchants from the database.
    lookup_field = 'merchant_id'            #Use 'merchant_id' instead of the default primary key for lookups

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
        """
        Register a new merchant
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            merchant = serializer.save()  #Creates a new merchant using MerchantManager


            #Generate and store an email verification token
            verification_token = generate_verification_token()
            if store_verification_token(merchant.email, verification_token):
                if send_verification_email(merchant.email, verification_token):
                    refresh = RefreshToken.for_user(merchant)
                    return Response({
                        'status': 'success',
                        'message': 'Merchant registered successfully, Please check your email to verify your account',
                        'data': {
                            'merchant_id': merchant.merchant_id,
                            'email': merchant.email,
                            'business_name': merchant.business_name,
                            'first_name': merchant.first_name,
                            'last_name': merchant.last_name,
                            'access_token': str(refresh.access_token),
                            'refresh_token': str(refresh),
                        }
                    }, status=status.HTTP_201_CREATED)
                else:
                    return Response({
                        'status': 'warning',
                        'message': 'Merchant registered but verification email failed to send. Please contact support',
                        'data': {
                            'merchant_id': merchant.merchant_id,
                            'email': merchant.email,
                            'business_name': merchant.business_name,
                            'first_name': merchant.first_name,
                            'last_name': merchant.last_name,
                        }
                    }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                
        return Response({
            'status': 'error',
            'message': 'Registration failed',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['GET'])
    def verify_email(self, request):
        """
        Verify merchant's email using a token sent via email
        """
        email = request.query_params.get('email')
        token = request.query_params.get('token')
        
        if not email or not token:
            return Response({
                'status': 'error',
                'message': 'Email and token are required'
            }, status=status.HTTP_400_BAD_REQUEST)
        

        if verify_token(email, token):
            try:
                merchant = Merchant.objects.get(email=email)
                merchant.is_email_verified = True
                merchant.save()

                return Response({
                    'status': 'success',
                    'message': 'Email verified successfully'
                }, status=status.HTTP_200_OK)
            except Merchant.DoesNotExist:
                return Response({
                    'status': 'error',
                    'message': 'Merchant not found'
                }, status=status.HTTP_404_NOT_FOUND)
        
        return Response({
            'status': 'error',
            'message': 'Invalid or expired verification token'
        }, status=status.HTTP_400_BAD_REQUEST)


    @action(detail=False, methods=['POST'])
    def signin(self, request):
        """
        Authenticate  a merchant and issue JWT tokens if credentials are valid.
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email'] 
            password = serializer.validated_data['password']

            merchant = authenticate(email=email, password=password)

            if merchant:
                if not merchant.is_email_verified:
                    #generate a  new verification token and send email again
                    verification_token = generate_verification_token()
                    if store_verification_token(merchant.email, verification_token):
                        send_verification_email(merchant.email, verification_token)
                    return Response({
                        'status': 'error',
                        'message': 'Email not verified. A new verification link has been sent to your email'
                    }, status=status.HTTP_403_FORBIDDEN)
                refresh = RefreshToken.for_user(merchant)
                return Response({
                    'status': 'success',
                    'message': 'Login successful',
                    'data': {
                        'access_token': str(refresh.access_token),
                        'refresh_token': str(refresh),
                        'merchant_id': merchant.merchant_id,
                        'email': merchant.email,
                        'business_name': merchant.business_name,
                        'is_email_verified': merchant.is_email_verified
                    }
                }, status=status.HTTP_200_OK)
            
        return Response({
            'status': 'error',
            'message': 'Invalid credentials'
        }, status=status.HTTP_401_UNAUTHORIZED)
    
    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve merchant's  profile details 
        """
        instance = self.get_object()

        #Check if the requesting user is the profile owner
        if not request.user.is_authenticated or request.user.merchant_id != instance.merchant_id:
            return Response({
                'status': 'error',
                'message': 'Access denied: You do not have permission to view this profile'
            }, status=status.HTTP_403_FORBIDDEN)
        if not instance.is_email_verified:
            return Response({
                'status': 'error',
                'message': 'Please verify your email before accessing your profile'
            }, status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(instance)
        return Response({
            'status': 'success',
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





















