
from rest_framework import viewsets, status,permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Merchant
from .serializers import MerchantRegistrationSerializer, MerchantProfileSerializer, MerchantLoginSerializer, VerifyEmailSerializer
from django.shortcuts import get_object_or_404
import hashlib
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework import serializers
from .utils import generate_otp, send_otp_email, store_verification_code, verify_code

class MerchantViewSet(viewsets.ModelViewSet):
    """
    Viewset for handling all merchant operations including, registration, 
    authentication, and profile management
    """

    queryset = Merchant.objects.all()
    lookup_field = 'merchant_id'

    def get_serializer_class(self):
        """
        Return appropriate serializer class based on the action being performed
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
        Return appropriate permission class based on the action being performed
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
            merchant = serializer.save()  #This will use create_user from MerchantManager

            verification_code = generate_otp()
            if store_verification_code(merchant.email, verification_code):

                if send_otp_email(merchant.email, verification_code):
                    refresh = RefreshToken.for_user(merchant)
                    return Response({
                        'status': 'success',
                        'message': 'Merchant registered successfully, Verification code sent: Enter code to verify email',
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
    
    @action(detail=False, methods=['POST'])
    def verify_email(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        code = serializer.validated_data['code']

        if verify_code(email, code):
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
            'message': 'Invalid or expired verification code'
        }, status=status.HTTP_400_BAD_REQUEST)


    @action(detail=False, methods=['POST'])
    def signin(self, request):
        """
        Authenticate merchant
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email'] 
            password = serializer.validated_data['password']

            merchant = authenticate(email=email, password=password)

            if merchant:
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
        Retrieve merchant profile
        """
        instance = self.get_object()

        #Check if the requesting user is the profile owner
        if not request.user.is_authenticated or request.user.merchant_id != instance.merchant_id:
            return Response({
                'status': 'error',
                'message': 'Access denied: You do not have permission to view this profile'
            }, status=status.HTTP_403_FORBIDDEN)
        serializer = self.get_serializer(instance)
        return Response({
            'status': 'success',
            'message': 'Merchant profile retrieved successfully',
            'data': serializer.data
        }, status=status.HTTP_200_OK)
    
    def get_object(self):
        """
        Override to lookup merchant by merchant_id instead of pk
        """
        lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
        merchant_id = self.kwargs.get(lookup_url_kwarg or self.lookup_field)
        if not merchant_id:
            raise serializers.ValidationError('Merchant ID is required')
        merchant = get_object_or_404(Merchant, merchant_id=merchant_id)
        # return get_object_or_404(Merchant, merchant_id=merchant_id)
        self.check_object_permissions(self.request, merchant)
        return merchant