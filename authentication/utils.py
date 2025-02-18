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
# from django.core.mail import get_connection, EmailMessage



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








# def store_verification_code(email, code):
#     """Store the verification code in Redis.

#     :param email: Email address for the verification code
#     :type email: str
#     :param code: Verification code
#     :type code: str
#     """
#     try:
#         redis_client.setex(
#             f"email_verification:{email}",
#             settings.EMAIL_VERIFICATION_TIMEOUT,
#             code
#         )
#         logger.info(f"Verification code stored for {email}")
#         return True
#     except redis.RedisError as e:
#         logger.error(f"Redis error storing verification code: {str(e)}")
#         return False

# def verify_code(email, code):
#     """
#     Verify the code against the stored code in Redis.

#     :param email: Email address for the verification code
#     :type email: str
#     :param code: Verification code
#     :type code: str
#     :return: True if the code matches, False otherwise
#     :rtype: bool
#     """
#     try:
#         stored_code = redis_client.get(f"email_verification:{email}")
#         if not stored_code:
#             logger.warning(f"No verification code found for {email}")
#             return False
#         return stored_code == code
#     except redis.RedisError as e:
#         logger.error(f"Redis error verifying code: {str(e)}")
#         return False



# def generate_otp():
#     """Generate a 6-digit OTP"""
#     return str(random.randint(100000, 999999))

# def send_test_email():
#     """Send a test email on server restart to verify SMTP configuration."""
#     subject = "SMTP Test Email from Django"
#     message = "Hello,\n\nThis is a test email sent automatically when the server restarts.\n\nThank you!"
#     sender_email = "info@prudytelecom.com.ng"  # Your email
#     recipient_list = ["info@prudytelecom.com.ng"]  # Replace with your email to receive the test message

#     try:
#         send_mail(subject, message, sender_email, recipient_list)
#         print("Test email sent successfully!")
#     except Exception as e:
#         print(f"Error sending test email: {e}")

# def send_otp_email(email, otp):
#     """Send OTP verification email to the merchant"""
#     subject = "Your OTP Verification Code"
#     message = f"Hello,\n\nYour OTP verification code is: {otp}\n\nUse this code to verify your email address.\n\nThank you!"
#     sender_email = "info@prudytelecom.com.ng"
    
#     try:
#         send_mail(subject, message, sender_email, [email])
#         return True
#     except Exception as e:
#         print(f"Error sending OTP email: {e}")
#         return False
















































# def get_hostinger_cert():
#     try:
#         response = requests.get('https://smtp.hostinger.com')
#         return ssl.get_server_certificate(('smtp.hostinger.com', 465))
#     except Exception as e:
#         logger.error(f"Error getting certificate: {str(e)}")
#         return None

# # Initialize email SSL context
# try:
#     email_context = ssl.create_default_context()
# except Exception as e:
#     logger.error(f"Error creating email SSL context: {str(e)}")
#     email_context = None

# def generate_verification_code():
#     """Generate a random 6-digit verification code.

#     :return: Random 6-digit code
#     :rtype: str
#     """
#     return ''.join(random.choices(string.digits, k=settings.VERIFICATION_CODE_LENGTH))










































# def send_verification_email(email, code):
#     """
#     Send a verification email using Django's send_mail
#     """
#     subject='Verify Your Email Address'
#     html_message = f"""
#     <html>
#     <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
#         <h2>Email Verification</h2>
#         <p>Thank you for registering. Your verification code is:</p>
#         <h1 style="color: #4CAF50; font-size: 32px; letter-spacing: 2px;">{code}</h1>
#         <p>This code will expire in {settings.EMAIL_VERIFICATION_TIMEOUT // 60}.</p>
#     </body>
#     </html> 
#     """
#     plain_message = f'Your verification code is: {code}. This code will expire in {settings.EMAIL_VERIFICATION_TIMEOUT // 60} minutes.'
#     send_mail(
#         subject,
#         plain_message,
#         f'{settings.EMAIL_HOST_USER}',
#         [email],
#         html_message=html_message
    
# )

# #     try:
# #         #Create a custom SSL context that doesn't verify certificates
# #         context = ssl.create_default_context()
# #         context.check_hostname = False
# #         context.verify_mode = ssl.CERT_NONE

# #         #Create a connection with the custom SSL context
# #         connection = get_connection(
# #             backend=settings.EMAIL_BACKEND,
# #             host=settings.EMAIL_HOST,
# #             port=settings.EMAIL_PORT,
# #             username=settings.EMAIL_HOST_USER,
# #             password=settings.EMAIL_HOST_PASSWORD,
# #             use_ssl=settings.EMAIL_USE_SSL,
# #             use_tls=settings.EMAIL_USE_TLS,
# #             ssl_context=context,
# #         )

# #         email_message = EmailMessage(
# #             subject=subject,
# #             body=html_content,
# #             from_email=settings.FROM_EMAIL,
# #             to=[email],
# #             connection=connection,
# #         )
# #         email_message.content_subtype = 'html'
#     #     result = email_message.send()
#     #     if result == 1:
#     #         logger.info(f'Verification email sent successfully to {email}')
#     #         return True
#     #     else:
#     #         logger.warning(f'Failed to send verification email to {email}')
#     #         return False
#     # except Exception as e:
#     #     logger.error(f'Error sending verification email: {str(e)}')
#     #     return False



#     #     from django.core.mail import EmailMessage
#     #     email_msg = EmailMessage(
#     #         subject=subject,
#     #         from_email=settings.FROM_EMAIL,
#     #         to=[email],
#     #         body=html_content,
            
#     #     )
#     #     email_msg.content_subtype = 'html'
#     #     if email_context:
#     #         email_msg.send()
#     #         logger.info(f"Verification email sent successfully to {email}")
#     #         return True
#     #     else:
#     #         logger.error(f"Failed to send verification email to {email}")
#     #         return False
#     # except Exception as e:
#         # logger.error(f"Error sending verification email: {str(e)}")
#         # return False
#     # message = Mail(
#     #     from_email=settings.FROM_EMAIL,
#     #     to_emails=email,
#     #     subject=subject,
#     #     html_content=html_content
#     # )
#     # try:
#     #     sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
#     #     sg.send(message)
#     #     response = sg.send(message)
#     #     if response.status_code in [200, 201, 202]:
#     #         logger.info(f"Verification email sent to {email}")
#     #         return True
#     #     else:
#     #         logger.error(f'SendGrid API error: Status code {response.status_code}')
#     #     return False
#     # except Exception as e:
#     #     print(f"Failed to send verification email: {str(e)}")
#     #     return False
        






