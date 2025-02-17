from django.apps import AppConfig
from django.core.mail import send_mail
from authentication.utils import send_test_email


class AuthenticationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'authentication'

    def ready(self):
        """Run email test when the server starts."""
        print("Server restarted - Sending test email...")
        send_test_email()