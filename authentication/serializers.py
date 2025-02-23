# import serializers to convert complex datatypes like django model to pyhton datatypes that can be easily rendered in JSON, XML, etc
from rest_framework import serializers
# import Merchant model from the current directory
from .models import Merchant
import hashlib
import os
import uuid
# customise TokenObtainPairSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
# imports to display the expiration timestamps for access JWT & refresh JWT
from django.conf import settings
from datetime import datetime
from .utils import generate_verification_token, store_verification_token, send_verification_email, store_merchant_data, clear_merchant_data
from django.contrib.auth.hashers import make_password
import logging


logger = logging.getLogger(__name__)



###############################################################################################################

# create a serializer for admin users
class AdminSerializer(serializers.ModelSerializer):
    # configure password field
    password = serializers.CharField(write_only=True,  # Exclude password from read operations
                                     required=True,  # Make password required during creation
                                     style={'input_type': 'password'},
                                     min_length=8,
                                     max_length=100,
                                     error_messages={
                                         'min_length': 'Password must be at least 8 characters long.',
                                         'max_length': 'Password must not exceed 100 characters.'
                                     }
                                     )

    class Meta:
        model = Merchant
        # allow superusers to manage all merchant verification statuses
        fields = '__all__'                          
        
        # fields that can be viewed but not modified via API        
        read_only_fields = ['merchant_id', 'createdAt', 'updatedAt']

    # create a superuser
    def create(self, validated_data):
        """Create a new superuser merchant with the provided validated data.

        :param validated_data: Dictionary containing the validated data from the request body
        :type validated_data: dict
        :return: Created merchant instance
        :rtype: Merchant
        """        
        # create a new superuser merchant instance using the MerchantManager with the validated data
        # NOTE: MerchantManager.create_superuser method handles password hashing
        merchant = Merchant.objects.create_superuser(**validated_data) 
        
        # return the created superuser merchant instance
        return merchant

    # ensure only superusers can edit certain fields
    def validate(self, data):
        """Validate that only superusers can modify restricted fields.

        :param data: Dictionary containing the fields to validate from the request body
        :type data: dict
        :raises serializers.ValidationError: If a regular user attempts to modify restricted fields
        :return: Validated data dictionary
        :rtype: dict
        """        
        request = self.context.get('request')
        if request and not request.user.is_admin:
            # Prevent non-superusers from editing certain fields
            for field in ['is_staff', 'is_admin', 'is_email_verified', 'is_nin_verified', 'is_bvn_verified', 'is_business_cac_verified', 'is_kyc_verified']:
                if field in data:
                    raise serializers.ValidationError(f"Only superadmin can edit the '{field}' field.")
        
        # return the dict containing the fields & values sent in the request body to update/create a merchant
        return data

    # regardless of PUT/PATCH request, a custom update method must handle password changes securely
    # - else it would try to save the raw password str
    def update_password(self, instance, validated_data):
        """Update user password by hashing & saving it.

        :param instance: The merchant instance to be updated
        :type instance: Merchant
        :param validated_data: Dictionary containing the validated data including password
        :type validated_data: dict
        :return: Updated merchant instance
        :rtype: Merchant
        """        
        # Handle the password updates seperately with the set_password method for hashing
        if 'password' in validated_data:
            # remove raw str password from validated_data
            password = validated_data.pop('password')
            instance.set_password(password)
            # save the hashed password
            instance.save()

        # update other fields normally with super().update
        # return the update           
        return super().update(instance, validated_data)

# resolve error when trying to get a token: AttributeError at /api/v1/token/ 'Merchant' object has no attribute 'id
# - Simple JWT is looking for an 'id' field, but the custom user model (Merchant) uses 'merchant_id' instead    
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    # configure serializer to use email instead of username for authentication
    username_field = 'email'

    # custom method to enhance JWT token with additional claims
    # https://django-rest-framework-simplejwt.readthedocs.io/en/latest/customizing_token_claims.html#customizing-token-claims
    @classmethod
    def get_token(cls, user):
        """Generate JWT token with custom claims for the superuser merchant.

        :param user: Generate a token for Merchant instance
        :type user: Merchant
        :return: JWT token with custom claims 
        :rtype: rest_framework_simplejwt.tokens.Token
        """
        # get the base token from parent class
        token = super().get_token(user)

        # add custom claims to token payload
        # avoid sensitive data + mutable data, include claims for user ID, authorisation checks, frequently accessed user info
        # public custom claims
        token['merchant_id'] = str(user.merchant_id)
        token['email'] = user.email
        token['role'] = user.role
        # private custom claims
        token['is_staff'] = user.is_staff
        token['is_admin'] = user.is_superuser 
        
        # del token['user_id']       

        # return token    
        return token    
    
    # include merchant_id in the JWT token response
    def validate(self, attrs):
        """Validate & process serializer data.

        :param attrs: Dictionary of fields values to validate
        :type attrs: dict
        :return: Validated data with merchant_id & expiration times for JWT tokens
        :rtype: dict
        """
        # call parent class's validate() method to perform default JWT validation & get token data
        data = super().validate(attrs)        

        # get the current time
        current_time = datetime.now()

        # calcalate expiration times for access & refresh tokens
        # access the expiration period for the JWT tokens in settings.py
        access_token_expiration = current_time + settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME']
        refresh_token_expiration = current_time + settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME']

        # format timestamps 
        # add timestamps to the data dictionary so it can be returned
        data['refresh_token_expires_at'] = refresh_token_expiration.strftime('%d-%m-%Y %H:%M:%S')
        data['access_token_expires_at'] = access_token_expiration.strftime('%d-%m-%Y %H:%M:%S')

        # add merchant_id to the response
        # data['merchant_id'] = str(self.user.merchant_id)

        # return data
        return data

#Serializer for Merchant Registration

class MerchantRegistrationSerializer(serializers.ModelSerializer):
    """
    This serializer handles merchant registration, including password validation 
    and email verification token generation
    """

    #Define password fields with restrictions: write-only, minimum length of 8, and required
    password = serializers.CharField(write_only=True, min_length=8, required=True)
    confirm_password = serializers.CharField(write_only=True, min_length=8, required=True)

    class Meta:
        """
        Meta class specifies the model and the fields to be serialized .
        """
        model = Merchant        #The serializer is linked to the Merchant Model

        #Fields included in the API request
        fields = ['first_name', 'last_name', 'middle_name', 'business_name', 'bvn', 'email', 'phone', 'password', 'confirm_password']

        #Extra fields that exist in the model but aren't required in the request
        extra_fields = ['createdAt', 'updatedAt', 'role', 'is_email_verified']


    def validate(self, data):
        """
        Custom validation to ensure:
        1. Password and confirm-password match
        2. BVN (Bank Verification Number) is provided
        """

        #Check if password match
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({'password': 'Passwords do not match'})
        
        #Ensure BVN is provided
        if not data.get('bvn'):
            raise serializers.ValidationError({'bvn': 'BVN is required'})
        
        return data             #Return validated data if all checks pass
    

    
    def create(self, validated_data):
    # Remove confirm_password field
        validated_data.pop('confirm_password')

        # Get and hash the password
        password = validated_data.pop('password')
        password_hash = make_password(password)
        validated_data['password'] = password_hash

        # Generate the verification token
        token = generate_verification_token()

        # Convert merchant data to strings
        merchant_data = {k: str(v) for k, v in validated_data.items()}

        logger.info(f"Generated token: {token}")
        logger.info(f"Storing merchant data for {merchant_data['email']}")

        # Store merchant data
        if store_merchant_data(merchant_data['email'], merchant_data, token):
            logger.info(f"Merchant data stored for {merchant_data['email']}")
        
        # Store verification token in Redis
            if store_verification_token(merchant_data['email'], token):
                logger.info(f"Verification token stored for {merchant_data['email']}")
            
                # Send verification email
                if send_verification_email(merchant_data['email'], token):
                    logger.info(f"Verification email sent to {merchant_data['email']}")
                    return True
                else:
                    clear_merchant_data(merchant_data['email'])
                    raise serializers.ValidationError('Failed to send verification email')
            else:
                raise serializers.ValidationError('Failed to store verification token')
        else:
            raise serializers.ValidationError('Failed to process registration')

    



#Serializer for Email Verification
class VerifyEmailSerializer(serializers.Serializer):
    """
    This serializer is used for verifying a merchant's email using a token.
    """

    email = serializers.EmailField()            #The merchant's email
    token = serializers.CharField()             #Verification token sent via email

    
       
#Serializer for Merchant Login       
class MerchantLoginSerializer(serializers.Serializer):
    """
    This serializer handles merchant login by accepting email and password.
    """
    email = serializers.EmailField(required=True)           #Email field (required)
    password = serializers.CharField(required=True)         #Password field (required)




#Serializer for Merchant Profile
class MerchantProfileSerializer(serializers.ModelSerializer):
    """
    This serializer is used to fetch a merchant's profile details
    """
    class Meta:
        """
        Meta class specifies the Merchant model and the fields to be serialized.
        """
        model = Merchant        #Linking serializer to the Merchant model

        #Fields included in profile response      
        fields = ['first_name', 'last_name', 'middle_name', 'business_name', 'email', 'phone', 'is_email_verified',
                  'role', 'createdAt', 'updatedAt'
        ]

