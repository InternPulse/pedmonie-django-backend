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




logger = logging.getLogger(__name__)

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

    # base_url = settings.FRONTEND_URL
    verification_url = urljoin(config('FRONTEND_URL'), f'/verify-email?email={email}&token={token}')
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








