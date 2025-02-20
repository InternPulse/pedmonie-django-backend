# Django model system for DB table definitions
from django.db import models

# UUID for generating unique identifiers
import uuid

# use Django's built-in authentication system
# import core Django auth classes for custom user model implementation
# provide core user functionality, user creation, support for permissions & groups, respectively
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator, MinLengthValidator, EmailValidator



##########################################################################################################

# add MerchantManager for custom user & superuser creation (modify the merchant model for admin users)
# extend Django's authentication system with email-based authentication
# custom manager extends Django's BaseUserManager
class MerchantManager(BaseUserManager):
    # create a regular merchant user
    # use email for login, not username
    def create_user(self, email, password=None, **extra_fields):
        """Create & save a new merchant user.

        :param email: Merchant's email address
        :type email: str
        :param password: Password for authentication, defaults to None
        :type password: str, optional
        :param extra_fields: Additional fields for the merchant model
        :type extra_fields: dict
        :raises ValueError: If email invalid or not provided
        :return: New merchant user instance
        :rtype: Merchant
        """        
        # validate the presence of email
        # normalise the email to convert to lowercase & validate format
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)

        # create new user instance with email & additional fields
        user = self.model(email=email, **extra_fields)
        
        # use Django's built-in password hashing
        # - instead of storing password_hash manually
        user.set_password(password)

        # save the merchant user 
        # return the user
        user.save(using=self._db)
        return user

    # create & save a superadmin user with full privileges
    def create_superuser(self, email, password=None, **extra_fields):
        """Create & save a new superuser with admin privileges.

        :param email: Superuser's email address
        :type email: str
        :param password: Password for authentication, defaults to None
        :type password: str, optional
        :param extra_fields: Additional fields for the merchant model
        :type extra_fields: dict
        :raises ValueError: If email invalid or not provided
        :raises ValueError: If role is not set to superadmin
        :raises ValueError: If is_staff or is_superuser is not True
        :return: New superuser merchant instance
        :rtype: Merchant
        """
        # validate the presence of email
        # normalise the email to convert to lowercase & validate format
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
       
        # ensure superadmin role for superuser creation
        extra_fields.setdefault('role', 'superadmin')
        if extra_fields.get('role') != 'superadmin':
            raise ValueError('Superuser must have role=superadmin.')
        
        # Django auth-specific field to ensure superuser has admin access
        extra_fields.setdefault('is_staff', True)        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superadmin must have is_staff=True.')
        
        # Django auth-specific field from PermissionsMixin to ensure superuser has full system permissions
        extra_fields.setdefault('is_superuser', True)        
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superadmin must have is_superuser=True.')

        # create superuser using base user creation method
        return self.create_user(email, password, **extra_fields)

# Merchant model inherits from AbstractBaseUser for authentication capabilities (JWT implementation handled with REST framework)
class Merchant(AbstractBaseUser, PermissionsMixin):
    """Merchant model for storing user account information and KYC details.
    Uses email as the unique identifier for login (USERNAME_FIELD).

    :param AbstractBaseUser: Django's user base user class providing core functionality
    :type AbstractBaseUser: django.contrib.auth.models.AbstractBaseUser
    :param PermissionsMixin: Add support for permissions & groups
    :type PermissionsMixin: django.contrib.auth.models.PermissionsMixin
    :return: Merchant instance
    :rtype: Merchant
    """
    # basic merchant info
    
    merchant_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sn = models.CharField(max_length=50,unique=True, db_index=True, verbose_name="Serial Number", blank=True)
    

    # def __str__(self):
    #     return self.sn
    first_name = models.CharField(max_length=50, validators=[MinLengthValidator(2)], default='')   
    last_name = models.CharField(max_length=50, validators=[MinLengthValidator(2)])
    middle_name = models.CharField(max_length=50, blank=True, help_text=_('(Optional)'))
    business_name = models.CharField(max_length=50, validators=[MinLengthValidator(2)])
    email = models.EmailField(max_length=50, unique=True, validators=[EmailValidator()])
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+234'. Up to 15 digits allowed.")
    phone = models.CharField(max_length=15)
    
    
    # account status & role
    is_email_verified = models.BooleanField(default=False)    
    role = models.CharField(max_length=20, choices=[('merchant', 'Merchant'), ('superadmin', 'Super Admin')], default='merchant')
    # total_balance = models.DecimalField(max_digits=19, decimal_places=4, default=0.0)
    is_staff = models.BooleanField(default=False)  # Allows superadmin access to Django Admin

    # KYC verification fields
    nin = models.CharField(max_length=30, unique=True, null=True, blank=True)
    is_nin_verified = models.BooleanField(default=False)
    bvn = models.CharField(max_length=30, unique=True, null=True, blank=True, help_text=_('(Bank Verification Number)'))
    is_bvn_verified = models.BooleanField(default=False)
    cac_number = models.CharField(max_length=30, unique=True, null=True, blank=True, help_text=_('(Corporate Affairs Commission)'))
    is_business_cac_verified = models.BooleanField(default=False)

    # document uploads
    id_card = models.ImageField(upload_to="id_cards/", null=True, blank=True)
    passport = models.ImageField(upload_to="passports/", null=True, blank=True)
    is_kyc_verified = models.BooleanField(default=False)

    # timestamps
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True) 
    


    # custom manager for creating users & superusers
    objects = MerchantManager()

    #Added id property for SimpleJWT compatibility
    @property
    def id(self):
        return self.merchant_id
      

    # specify email as the login identifier
    USERNAME_FIELD = 'email'

    # extra required fields during user creation
    REQUIRED_FIELDS = ['first_name', 'last_name', 'business_name', 'phone']

    # resolve error about Django's built-in authentication system permissions at the db level before migrations
    # both the default Django User model & Merchant model inherit from PermissionsMixin
    # PermissionsMixin has fields groups + user_permissions
    # both model try to create reverse relationships with the name user_set to group + permission models
    # hence ERRORS: auth.User.groups: (fields.E304) Reverse accessor 'Group.user_set' for 'auth.User.groups' clashes with reverse accessor for 'authentication.Merchant.groups'.
    # fix: specify different related_name value for Merchant model to avoid clashing with User model relationships
    class Meta:
        # set merchant permissions
        permissions = [ 
            ("manage_balance", "Can manage merchant balance"),
            ("verify_kyc", "Can verify merchant KYC details"),
            ("manage_orders", "Can manage merchant orders"),
            ("manage_wallets", "Can manage merchant wallets"),
            ("manage_transactions", "Can manage merchant transactions"),
            ("manage_merchants", "Can manage other merchants"),
        ] 
        default_related_name = 'merchants' # this fixes relationship clash
        db_table = 'merchants'

    # define a __str__ method for human-readable output
    # return merchant
    def __str__(self):
        """A human-readable string representation of the Science & Nature question object.

        :return: Return the merchant object
        :rtype: str
        """
        return f"({self.role}), {self.first_name} {self.last_name} {self.business_name}"
    def save(self, *args, **kwargs):
        if not self.sn:  # Only assign if 'sn' is empty
            last_merchant = Merchant.objects.order_by('-sn').first()
            if last_merchant and last_merchant.sn.isdigit():
                self.sn = str(int(last_merchant.sn) + 1)
            else:
                self.sn = "1"  # Start from 1 if no records exist
        super().save(*args, **kwargs)
    
        
    
