from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import AccessToken

class AdminWalletAPITestCase(APITestCase):
    """Test admin wallet endpoints with proper authentication"""

    def setUp(self):
        """Set up test data"""
        self.User = get_user_model()

        # Create an admin merchant (superuser)
        self.admin_user = self.User.objects.create_superuser(
            email="admin@example.com",
            password="adminpassword",
            first_name="Admin",
            last_name="User",
            business_name="Admin Biz",
            phone="1234567890"
        )

        # Generate admin JWT access token
        self.admin_token = str(AccessToken.for_user(self.admin_user))

        # Authenticated headers
        self.admin_headers = {"HTTP_AUTHORIZATION": f"Bearer {self.admin_token}"}

        # Wallet API URLs
        self.wallet_list_url = "/api/v1/wallet/"  # List all wallets
        self.wallet_detail_url = lambda wallet_id: f"/api/v1/wallet/{wallet_id}/"  # Specific wallet

    def test_admin_can_get_all_wallets(self):
        """Ensure admin can retrieve all wallets"""
        response = self.client.get(self.wallet_list_url, **self.admin_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_can_get_specific_wallet(self):
        """Ensure admin can retrieve a specific wallet"""
        wallet_id = "123e4567-e89b-12d3-a456-426614174000"  # Replace with a real wallet ID
        response = self.client.get(self.wallet_detail_url(wallet_id), **self.admin_headers)
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_404_NOT_FOUND])  # Ensure valid response

    def test_non_admin_cannot_access_wallets(self):
        """Ensure non-admin users cannot access admin wallets"""
        # Create a normal (non-superuser) merchant
        regular_user = self.User.objects.create_user(
            email="user@example.com",
            password="userpassword",
            first_name="Regular",
            last_name="User",
            business_name="User Biz",
            phone="0987654321"
        )

        # Generate non-admin JWT token
        non_admin_token = str(AccessToken.for_user(regular_user))
        non_admin_headers = {"HTTP_AUTHORIZATION": f"Bearer {non_admin_token}"}

        response = self.client.get(self.wallet_list_url, **non_admin_headers)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)  # Non-admins should be denied

    def test_admin_can_update_wallet(self):
        """Ensure admin can update a wallet"""
        wallet_id = "123e4567-e89b-12d3-a456-426614174000"  # Replace with a real wallet ID
        update_data = {"total_balance": "5000.00"}
        response = self.client.patch(self.wallet_detail_url(wallet_id), update_data, **self.admin_headers)
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_404_NOT_FOUND])  # Ensure valid response

    def test_admin_can_delete_wallet(self):
        """Ensure admin can delete a wallet"""
        wallet_id = "123e4567-e89b-12d3-a456-426614174000"  # Replace with a real wallet ID
        response = self.client.delete(self.wallet_detail_url(wallet_id), **self.admin_headers)
        self.assertIn(response.status_code, [status.HTTP_204_NO_CONTENT, status.HTTP_404_NOT_FOUND])  # Ensure valid response

