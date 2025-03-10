import random
import uuid
import string
from django.conf import settings
import redis
import logging
from rest_framework import response
from django.core.mail import send_mail
import requests
import ssl
from urllib.parse import urljoin
from decouple import config
import cloudinary
import cloudinary.uploader
import cloudinary.api




logger = logging.getLogger(__name__)

cloudinary.config(
    cloud_name = config('CLOUDINARY_CLOUD_NAME'),
    api_key = config('CLOUDINARY_API_KEY'),
    api_secret = config('CLOUDINARY_API_SECRET')
)

redis_client = redis.Redis(
    host=config('REDIS_HOST'),
    port=config('REDIS_PORT'),
    db=config('REDIS_DB'),
    decode_responses=True,
    username=config('REDIS_USERNAME'),
    password=config('REDIS_PASSWORD'),    
)


def generate_verification_token():
    """
    Generate a unique verification token
    """
    return str(uuid.uuid4())

    
def store_verification_token(email, token):
    try:
        sanitized_email = email.replace('@', '_').replace('.', '_')  # Sanitize email
        logger.info(f"Storing token for {sanitized_email}: {token}")
        result = redis_client.setex(
            f'email_verification:{sanitized_email}',
            int(config('EMAIL_VERIFICATION_TIMEOUT')),
            token
        )
        logger.info(f"Redis setex result: {result}")
        logger.info(f"Token stored successfully for {sanitized_email}")
        return True
    except redis.RedisError as e:
        logger.error(f"Redis error storing verification token for {email}: {str(e)}")
        return False

    
def store_merchant_data(email, merchant_data):
    """
    Store merchant registration data and verification token
    """
    try:

        redis_client.hset(
            f'merchant_registration:{email}',
            mapping=merchant_data
        )

        redis_client.expire(
            f'merchant_registration:{email}',
            int(config('EMAIL_VERIFICATION_TIMEOUT'))
        )
        return True
    except redis.RedisError as e:
        logger.error(f'Redis error storing merchant data: {str(e)}')
        return False

def get_merchant_data(email):
    """
    Retrieve stored merchant data from redis
    """
    try:
        data = redis_client.hgetall(f'merchant_registration:{email}')
        if data:
            return data
        return None
    except redis.RedisError as e:
        logger.error(f'Redis error retrieving merchant data: {str(e)}')
        return False

def clear_merchant_data(email):
    """
    Clear merchant data and verification token in Redis
    """
    try:
        redis_client.delete(f'merchant_registration{email}')
        redis_client.delete(f'email_verification:{email}')
        return True
    except redis.RedisError as e:
        logger.error(f'Redis error clearing merchant data: {str(e)}')
        return False
    




def verify_token(email, token):
    try:
        sanitized_email = email.replace('@', '_').replace('.', '_')
        stored_token = redis_client.get(f'email_verification:{sanitized_email}')
        if not stored_token:
            logger.warning(f'No verification token found for {sanitized_email}')
            return False

        logger.info(f"Comparing token: {stored_token} with {token}")
        if stored_token == token:
            redis_client.delete(f'email_verification:{sanitized_email}')
            return True
        return False
    except redis.RedisError as e:
        logger.error(f'Redis error verifying token: {str(e)}')
        return False
 



def send_verification_email(email, token):
    """
    Send verification link email to the merchant
    :param email: recipient email address
    :rtype email: str
    :param token: Verification token
    :type token: str
    """

    base_url = config('FRONTEND_URL')
    verification_url = urljoin(base_url, f'verify-email?email={email}&token={token}')
    print(f'{verification_url}')
    subject = "Verify your Email Address"
    message = f"""Hello,
    Please verify your email by clicking on the link below:
    {verification_url}
    This link will expire in {config('EMAIL_VERIFICATION_TIMEOUT')} minutes.
    Thank you!
    """
    sender_email = config('DEFAULT_FROM_EMAIL')
    try:
        send_mail(subject, message, sender_email, [email])
        logger.info(f'Verification email sent to {email}')
        return True
    except Exception as e:
        logger.error(f'Error sending verification email: {e}')
        return False


def verify_nin(self, bvn, first_name=None, last_name=None, date_of_birth=None):
    """
    Documentation: https://developers.korapay.com/docs/nigeria-nin
    """
    try:
        #Korapay API endpoint for NIN verirication
        url = "https://api.korapay.com/merchant/api/v1/identities/ng/nin"

        headers = {
            "Authorization": f"Bearer {config('KORAPAY_SECRET_KEY')}",
            "Content-Type": "application/json"
        }
        
        formatted_DOB = None
        if date_of_birth:
            dob_parts = date_of_birth.split('-')
            if len(dob_parts) == 3:
                formatted_DOB = f"{dob_parts[2]}-{dob_parts[1]}-{dob_parts[0]}"

        payload = {
            "reference": "merchant.nin",
            "firstname": "merchant.first_name",
            "lastname": "merchant.last_name",
            "verification_consent": true
        }

        response = requests.post(url, json=payload, headers=headers)
        response_data = response.json()

        #Log the rrsponse for debugging
        logger.debug(f'Korapay NIN verification response: {response_data}')

        if response.status_code == 200 and response_data.get('status') == True:
            data = response_data.get('data', {})
            is_verified = data.get('verification_status') == 'success'

            return {
                'status': 'success' if is_verified else 'error',
                'message': 'NIN verification successful' if is_verified else 'NIN verification failed',
                'data': data,
                'response_data': response_data
            }
        else:
            return {
                'status': 'error',
                'message': response_data.get('message', 'NIN verification failed'),
                'errors': response_data.get('errors', {}),
                'response_data': response_data
            }
    except Exception as e:
        logger.error(f'Error during NIN verification: {str(e)}')
        return {
            'status': 'error',
            'message': 'Error connecting to verification service.',
            'data': {'detail': str(e)}
        }
    

def verify_bvn(self, bvn, first_name=None, last_name=None, date_of_birth=None):
    """
    Verify BVN using KORAPAY
    """

    try:
        url = 'https://api.korapay.com/merchant/api/v1/identities/ng/bvn'

        headers = {
            "Authorization": f"Bearer {config('KORAPAY_SECRET_KEY')}",
            "Content-Type": "application/json"
        }
        formatted_DOB = None
        if date_of_birth:
            dob_parts = date_of_birth.split('-')
            if len(dob_parts) == 3:
                formatted_DOB = f"{dob_parts[2]}-{dob_parts[1]}-{dob_parts[0]}"

        payload = {
            "reference": "merchant.bvn",
            "firstname": "merchant.first_name",
            "lastname": "merchant.last_name",
            "verification_consent": true
        }

        response = requests.post(url, json=payload, headers=headers)
        response_data = response.json()

        #Log the rrsponse for debugging
        logger.debug(f'Korapay BVN verification response: {response_data}')

        if response.status_code == 200 and response_data.get('status') == True:
            data = response_data.get('data', {})
            is_verified = data.get('verification_status') == 'success'

            return {
                'status': 'success' if is_verified else 'error',
                'message': 'BVN verification successful' if is_verified else 'BVN verification failed',
                'data': data,
                'response_data': response_data
            }
        else:
            return {
                'status': 'error',
                'message': response_data.get('message', 'BVN verification failed'),
                'errors': response_data.get('errors', {}),
                'response_data': response_data
            }
    except Exception as e:
        logger.error(f'Error during BVN verification: {str(e)}')
        return {
            'status': 'error',
            'message': 'Error connecting to verification service.',
            'data': {'detail': str(e)}
        }
    



