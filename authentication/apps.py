from django.apps import AppConfig



class AuthenticationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'authentication'

    def ready(self):
        """Run email test when the server starts."""
        print("Server restarted - Sending test email...")
        send_test_email()