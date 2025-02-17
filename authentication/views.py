from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from authentication.models import Merchant
from authentication.serializers import AdminSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from authentication.utils import generate_otp, send_otp_email
from django.core.cache import cache  # Store OTP temporarily in Django cache

# Admin Registration
class AdminRegistrationView(APIView):
    """Create a new admin (superadmin)."""
    permission_classes = [AllowAny]

    def post(self, request):
        """Register a new admin."""
        serializer = AdminSerializer(data=request.data)
        if serializer.is_valid():
            admin = serializer.save(is_staff=True, is_superuser=True, role="superadmin")

            # Generate JWT token
            refresh = RefreshToken.for_user(admin)
            return Response({
                "message": "Admin registered successfully.",
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "user": AdminSerializer(admin).data
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#  Merchant Registration
# class MerchantRegistrationView(APIView):
#     """Create a new merchant."""
#     permission_classes = [AllowAny]

#     def post(self, request):
#         """Register a new merchant."""
#         serializer = AdminSerializer(data=request.data)
#         if serializer.is_valid():
#             merchant = serializer.save(role="merchant")

#             # Generate JWT token
#             refresh = RefreshToken.for_user(merchant)
#             return Response({
#                 "message": "Merchant registered successfully.",
#                 "access": str(refresh.access_token),
#                 "refresh": str(refresh),
#                 "user": AdminSerializer(merchant).data
#             }, status=status.HTTP_201_CREATED)

#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MerchantRegistrationView(APIView):
    """Register a new merchant and send OTP for email verification."""
    
    def post(self, request):
        """Register merchant and send OTP."""
        serializer = AdminSerializer(data=request.data)
        if serializer.is_valid():
            merchant = serializer.save(role="merchant")

            # Generate OTP
            otp = generate_otp()

            # Store OTP temporarily in Django cache (expires in 5 mins)
            cache.set(f"otp_{merchant.email}", otp, timeout=300)

            # Send OTP via email
            if send_otp_email(merchant.email, otp):
                return Response({
                    "message": "Merchant registered successfully. Please verify your email using the OTP sent to your inbox.",
                    "merchant_id": str(merchant.merchant_id)
                }, status=status.HTTP_201_CREATED)
            else:
                return Response({"error": "Failed to send OTP email."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# Verify Merchant Email using OTP
class VerifyOTPView(APIView):
    """Verify merchant email using OTP."""
    
    def post(self, request):
        """Check OTP and verify email."""
        email = request.data.get("email")
        otp_provided = request.data.get("otp")

        if not email or not otp_provided:
            return Response({"error": "Email and OTP are required."}, status=status.HTTP_400_BAD_REQUEST)

        # Retrieve OTP from cache
        otp_stored = cache.get(f"otp_{email}")

        if otp_stored and otp_provided == otp_stored:
            try:
                merchant = Merchant.objects.get(email=email)
                merchant.is_email_verified = True
                merchant.save()
                
                # Remove OTP from cache after successful verification
                cache.delete(f"otp_{email}")

                return Response({"message": "Email verified successfully!"}, status=status.HTTP_200_OK)
            except Merchant.DoesNotExist:
                return Response({"error": "Merchant not found."}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"error": "Invalid or expired OTP."}, status=status.HTTP_400_BAD_REQUEST)




#  Merchant Login (JWT)
class MerchantLoginView(APIView):
    """Login for merchants using email & password."""
    permission_classes = [AllowAny]

    def post(self, request):
        """Authenticate and return JWT token."""
        email = request.data.get("email")
        password = request.data.get("password")

        try:
            merchant = Merchant.objects.get(email=email)
            if merchant.check_password(password):
                refresh = RefreshToken.for_user(merchant)
                return Response({
                    "message": "Login successful.",
                    "access": str(refresh.access_token),
                    "refresh": str(refresh),
                    "user": AdminSerializer(merchant).data
                }, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Invalid password."}, status=status.HTTP_400_BAD_REQUEST)
        except Merchant.DoesNotExist:
            return Response({"error": "Merchant not found."}, status=status.HTTP_404_NOT_FOUND)
