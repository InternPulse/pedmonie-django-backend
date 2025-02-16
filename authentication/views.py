from django.http import HttpResponse
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import Merchant
from .serializers import AdminSerializer


# def MerchantCreateView(request):
#     return HttpResponse("Hello, World")

class MerchantCreateView(generics.CreateAPIView):
    """Handles merchant & admin registration."""
    queryset = Merchant.objects.all()
    serializer_class = AdminSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        """Custom user creation logic."""
        data = request.data.copy()

        # Ensure only 'merchant' and 'superadmin' roles are allowed
        role = data.get("role", "merchant").lower()
        if role not in ["merchant", "superadmin"]:
            return Response({"error": "Invalid role. Choose 'merchant' or 'superadmin'."}, status=status.HTTP_400_BAD_REQUEST)

        # Proceed with user creation
        serializer = self.get_serializer(data=data)
        if serializer.is_valid():
            user = serializer.save()

            # Generate JWT token
            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    "message": "User registered successfully.",
                    "access": str(refresh.access_token),
                    "refresh": str(refresh),
                    "user": AdminSerializer(user).data,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MerchantLoginView(generics.GenericAPIView):
    """Handles merchant/admin login & JWT generation."""
    serializer_class = AdminSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        """Authenticate user and return JWT token."""
        email = request.data.get("email")
        password = request.data.get("password")

        if not email or not password:
            return Response({"error": "Email and password are required."}, status=status.HTTP_400_BAD_REQUEST)

        # Authenticate user
        user = authenticate(email=email, password=password)
        if user:
            # Generate JWT tokens
            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    "message": "Login successful.",
                    "access": str(refresh.access_token),
                    "refresh": str(refresh),
                    "user": AdminSerializer(user).data,
                },
                status=status.HTTP_200_OK,
            )
        return Response({"error": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)

class MerchantLogoutView(generics.GenericAPIView):
    """Handles user logout by blacklisting the refresh token."""
    permission_classes = [AllowAny]

    def post(self, request):
        """Blacklist refresh token to log user out."""
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()  # Blacklist the refresh token
            return Response({"message": "Successfully logged out."}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"error": "Invalid token."}, status=status.HTTP_400_BAD_REQUEST)



