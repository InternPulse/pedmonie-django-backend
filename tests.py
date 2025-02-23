import http
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from unittest.mock import patch
from authentication.models import Merchant
from wallets.models import Wallet
from authentication.utils import verify_token, get_merchant_data, clear_merchant_data

class EmailVerificationTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.verify_email_url = reverse('merchant-verify-email')  # Update with your actual URL name
        self.valid_email = "test@example.com"
        self.valid_token = "33333"
        self.test_merchant_data = {
            'email': self.valid_email,
            'business_name': 'Test Business',
            'password': 'testpassword123',
            'phone': '+2341234567890',
            # Add other required merchant fields
        }

    @patch('authentication.views.verify_token')
    @patch('authentication.views.get_merchant_data')
    @patch('authentication.views.clear_merchant_data')
    def test_successful_verification(self, mock_clear_data, mock_get_data, mock_verify):
        # Mock the verification functions
        mock_verify.return_value = True
        mock_get_data.return_value = self.test_merchant_data
        mock_clear_data.return_value = None

        # Test data
        data = {
            'email': self.valid_email,
            'token': self.valid_token
        }

        # Make request
        response = self.client.post(self.verify_email_url, data)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['status'], 'True')
        self.assertTrue('access_token' in response.data['data'])
        self.assertTrue('refresh_token' in response.data['data'])

        # Verify database state
        merchant = Merchant.objects.get(email=self.valid_email)
        self.assertTrue(merchant.is_email_verified)
        self.assertEqual(merchant.business_name, self.test_merchant_data['business_name'])

        wallet = Wallet.objects.get(merchant=merchant)
        self.assertEqual(wallet.amount, 0.0)
        self.assertEqual(wallet.currency, 'NGN')
        # self.assertTrue(wallet.is_active)

    def test_missing_parameters(self):
        # Test missing email
        response = self.client.post(self.verify_email_url, {'token': self.valid_token})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Test missing token
        response = self.client.post(self.verify_email_url, {'email': self.valid_email})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch('authentication.views.verify_token')
    def test_invalid_token(self, mock_verify):
        mock_verify.return_value = False
        
        data = {
            'email': self.valid_email,
            'token': 'invalid_token'
        }
        
        response = self.client.post(self.verify_email_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['status'], False)
        self.assertEqual(response.data['message'], 'Invalid or expired verification token')

    @patch('authentication.views.verify_token')
    @patch('authentication.views.get_merchant_data')
    def test_expired_registration(self, mock_get_data, mock_verify):
        mock_verify.return_value = True
        mock_get_data.return_value = None
        
        data = {
            'email': self.valid_email,
            'token': self.valid_token
        }
        
        response = self.client.post(self.verify_email_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], 'Registration data expired or not found')