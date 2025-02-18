# import serializers to convert complex datatypes like django model to pyhton datatypes that can be easily rendered in JSON, XML, etc
from rest_framework import serializers

# import Merchant model from the current directory
from .models import Merchant

import hashlib
import os
import uuid
# from .utils import generate_otp, store_verification_code, verify_code, send_otp_email 
from .utils import generate_verification_token, store_verification_token, verify_token, send_verification_email
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
        fields = ['merchant_id',
                  'email',
                  'password',
                  'first_name',
                  'last_name',
                  'business_name',
                  'role',                  
                  'is_staff',
                  'is_superuser',
                  'is_email_verified',
                  'is_nin_verified',
                  'is_bvn_verified',
                  'is_business_cac_verified',
                  'is_kyc_verified',                  
                  ]
        
        # fields that can be viewed but not modified via API        
        read_only_fields = ['merchant_id', 'created_at', 'updated_at', 'total_balance']

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
        if request and not request.user.is_superuser:
            # Prevent non-superusers from editing certain fields
            for field in ['is_staff', 'is_superuser', 'is_email_verified', 'is_nin_verified', 'is_bvn_verified', 'is_business_cac_verified', 'is_kyc_verified']:
                if field in data:
                    raise serializers.ValidationError(f"Only superusers can edit the '{field}' field.")
        
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
        extra_fields = ['created_at', 'updated_at', 'role', 'total_balance', 'email_verification_code', 'is_email_verified']


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
        """
        Custom method to create a new Merchant instance.
        1. Removes the confim_password firld as it's not needed in the database.
        2. Hashes and stores the password securely.
        3. Creates a new Merchant instance using the 'create_user' method.
        4. Generates and stores an email verification token.
        5. Sends an email verificatiom message.
        """

        #Remove confirm_password since it's only needed for validation
        validated_data.pop('confirm_password')

        #Extract and remove password from  the validated data to handle it separately
        password = validated_data.pop('password')

        #Create a new Merchant instance with the provided data and hashed password
        merchant = Merchant.objects.create_user(password=password, **validated_data)

    
        #Generate, store and send token
        token = generate_verification_token()

        #Store the token  associated with the merchant's email 
        store_verification_token(merchant.email, token)

        #Send the verification email with the generated token
        send_verification_email(merchant.email, token)

        return merchant         #Return the created merchant instance 


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
    This serializer handles merchant login by acceptoing email and password.
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
                  'role', 'total_balance','created_at', 'updated_at'
        ]




















  #Generate and send verification code
        # code = generate_otp()
        # store_verification_code(merchant.email, code)
        # send_otp_email(merchant.email, code)

        # return merchant