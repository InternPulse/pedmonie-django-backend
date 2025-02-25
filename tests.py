import http
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from unittest.mock import patch
from authentication.models import Merchant
from wallets.models import Wallet
from authentication.utils import verify_token, get_merchant_data, clear_merchant_data
import unittest
from unittest.mock import patch, MagicMock
from authentication.utils import (
    generate_verification_token,
    store_verification_token,
    store_merchant_data,
    get_merchant_data,
    clear_merchant_data,
    verify_token,
    send_verification_email
)

class TestVerificationFunctions(unittest.TestCase):
    
    @patch('authentication.utils.redis_client')
    def test_generate_verification_token(self, mock_redis):
        token = generate_verification_token()
        self.assertIsInstance(token, str)
        self.assertEqual(len(token), 36)  # UUID4 length
    
    @patch('authentication.utils.redis_client')
    @patch('authentication.utils.config')
    def test_store_verification_token(self, mock_config, mock_redis):
        mock_config.return_value = '300'
        mock_redis.setex.return_value = True
        result = store_verification_token('test@example.com', 'token123')
        self.assertTrue(result)
    
    @patch('authentication.utils.redis_client')
    @patch('authentication.utils.config')
    def test_store_merchant_data(self, mock_config, mock_redis):
        mock_config.return_value = '300'
        mock_redis.hset.return_value = True
        mock_redis.expire.return_value = True
        result = store_merchant_data('test@example.com', {'name': 'Merchant'})
        self.assertTrue(result)
    
    @patch('authentication.utils.redis_client')
    def test_get_merchant_data(self, mock_redis):
        mock_redis.hgetall.return_value = {'name': 'Merchant'}
        result = get_merchant_data('test@example.com')
        self.assertEqual(result, {'name': 'Merchant'})
    
    @patch('authentication.utils.redis_client')
    def test_clear_merchant_data(self, mock_redis):
        mock_redis.delete.return_value = 1
        result = clear_merchant_data('test@example.com')
        self.assertTrue(result)
    
    @patch('authentication.utils.redis_client')
    def test_verify_token(self, mock_redis):
        mock_redis.get.return_value = 'token123'
        mock_redis.delete.return_value = True
        result = verify_token('test@example.com', 'token123')
        self.assertTrue(result)
    
    @patch('authentication.utils.send_mail')
    @patch('authentication.utils.config')
    def test_send_verification_email(self, mock_config, mock_send_mail):
        mock_config.side_effect = lambda key: {
            'FRONTEND_URL': 'https://frontend.com/',
            'EMAIL_VERIFICATION_TIMEOUT': '10',
            'DEFAULT_FROM_EMAIL': 'noreply@example.com'
        }[key]
        mock_send_mail.return_value = 1
        result = send_verification_email('test@example.com', 'token123')
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()



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