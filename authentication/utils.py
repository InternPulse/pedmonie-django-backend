import random
import uuid
import string
from django.conf import settings
import redis
# from sendgrid import SendGridAPIClient
# from sendgrid.helpers.mail import Mail
import logging
from rest_framework import response
from django.core.mail import send_mail
import requests
import ssl
from urllib.parse import urljoin




logger = logging.getLogger(__name__)

redis_client = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB,
    decode_responses=True    
)


def generate_verification_token():
    """
    Generate a unique verification token
    """
    return str(uuid.uuid4())

def store_verification_token(email, token):
    """
    Store the verification token in Redis.

    :param email: Email address for the verification token
    :type email: str
    :param token: Verification token
    :type token: str
    """
    try: 
        redis_client.setex(
            f'email_verification:{email}',
            settings.EMAIL_VERIFICATION_TIMEOUT,
            token
        )
        logger.info(f'verification token stored for {email}')
        return True
    except redis.RedisError as e:
        logger.error(f'Redis error storing verification token: {str(e)}')
        return False
def verify_token(email, token):
    """
    Verify the token againist the stored token on Redis.
    :param email: Email address for the verification token
    :type email: str
    :param token: verification token
    :type token: str
    :return: True if the token matches, False otherwise
    :rtype: bool
    """
    try:
        stored_token = redis_client.get(f'email_verification:{email}')
        if not stored_token:
            logger.warning(f'No verifcation token found for {email}')
            return False
        #if the token matches, delete it from Redis
        if stored_token == token:
            redis_client.delete(f'email_verification:{email}')
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

    base_url = settings.FRONTEND_URL
    verification_url = urljoin('http://localhost : 3000', f'/verify-email?email={email}&token={token}')
    print(f'{verification_url}')
    subject = "Verify your Email Address"
    message = f"""Hello,
    Please verify your email by clicking on the link below:
    {verification_url}
    This link will expire in {settings.EMAIL_VERIFICATION_TIMEOUT // 60} minutes.
    Thank you!
    """
    sender_email = 'info@prudytelecom.com.ng'
    try:
        send_mail(subject, message, sender_email, [email])
        logger.info(f'Verification email sent to {email}')
        return True
    except Exception as e:
        logger.error(f'Error sending verification email: {e}')
        return False
def send_test_email():
    """
    Send a test email on server restart to verify SMTP configuration.
    """
    subject = "SMTP Test Email from Django"
    message = "Hello,\n\nThis is a test email sent automatically when the server restarts.\n\nThank you!"
    sender_email = "info@prudytelecom.com.ng"
    recipient_list = ["overdoseofgodsblessings@gmail.com"]
    try:
        send_mail(subject, message, sender_email, recipient_list)
        print('Test email sent successfully!')
    except Exception as e:
        print(f'Error sending test email: {e}')







