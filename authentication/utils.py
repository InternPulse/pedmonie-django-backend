from django.core.mail import send_mail
import random

def generate_otp():
    """Generate a 6-digit OTP"""
    return str(random.randint(100000, 999999))

def send_test_email():
    """Send a test email on server restart to verify SMTP configuration."""
    subject = "SMTP Test Email from Django"
    message = "Hello,\n\nThis is a test email sent automatically when the server restarts.\n\nThank you!"
    sender_email = "info@prudytelecom.com.ng"  # Your email
    recipient_list = ["info@prudytelecom.com.ng"]  # Replace with your email to receive the test message

    try:
        send_mail(subject, message, sender_email, recipient_list)
        print("Test email sent successfully!")
    except Exception as e:
        print(f"Error sending test email: {e}")

def send_otp_email(email, otp):
    """Send OTP verification email to the merchant"""
    subject = "Your OTP Verification Code"
    message = f"Hello,\n\nYour OTP verification code is: {otp}\n\nUse this code to verify your email address.\n\nThank you!"
    sender_email = "info@prudytelecom.com.ng"
    
    try:
        send_mail(subject, message, sender_email, [email])
        return True
    except Exception as e:
        print(f"Error sending OTP email: {e}")
        return False
