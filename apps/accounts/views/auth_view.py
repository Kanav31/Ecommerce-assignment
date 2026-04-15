from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from drf_spectacular.utils import extend_schema

from apps.accounts.constants import Role
from apps.accounts.models import User
from apps.accounts.permissions import IsAdmin
from apps.accounts.serializers import (
    RegisterRequestSerializer,
    LoginRequestSerializer,
    UserResponseSerializer,
)
from apps.accounts.services import AuthService


class RegisterView(APIView):
    """POST /api/auth/register/"""
    permission_classes = [AllowAny]

    @extend_schema(
        request=RegisterRequestSerializer,
        responses={201: UserResponseSerializer},
        tags=['Auth'],
        summary='Register a new user',
    )
    def post(self, request):
        serializer = RegisterRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = AuthService.register_user(serializer.validated_data)
        return Response(UserResponseSerializer(user).data, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    """POST /api/auth/login/ — sets HttpOnly JWT cookies on success."""
    permission_classes = [AllowAny]

    @extend_schema(
        request=LoginRequestSerializer,
        responses={200: UserResponseSerializer},
        tags=['Auth'],
        summary='Login and receive JWT cookies',
    )
    def post(self, request):
        serializer = LoginRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = AuthService.login_user(
            email    = serializer.validated_data['email'],
            password = serializer.validated_data['password'],
        )

        response = Response(UserResponseSerializer(user).data, status=status.HTTP_200_OK)
        AuthService.set_jwt_cookies(response, user)
        return response


class LogoutView(APIView):
    """POST /api/auth/logout/"""
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=None,
        responses={200: None},
        tags=['Auth'],
        summary='Logout and clear JWT cookies',
    )
    def post(self, request):
        response = Response({'message': 'Logged out successfully.'}, status=status.HTTP_200_OK)
        AuthService.clear_jwt_cookies(response)
        return response


class MeView(APIView):
    """GET /api/auth/me/"""
    permission_classes = [IsAuthenticated]

    @extend_schema(
        responses={200: UserResponseSerializer},
        tags=['Auth'],
        summary='Get current authenticated user',
    )
    def get(self, request):
        return Response(UserResponseSerializer(request.user).data, status=status.HTTP_200_OK)


class RefreshTokenView(APIView):
    """POST /api/auth/refresh/ — issues a new access token using the refresh cookie."""
    permission_classes = [AllowAny]

    @extend_schema(request=None, responses={200: None}, tags=['Auth'], summary='Refresh access token')
    def post(self, request):
        cookie_settings = AuthService.get_cookie_settings()
        raw_refresh = request.COOKIES.get(cookie_settings['REFRESH_COOKIE_NAME'])

        if not raw_refresh:
            raise AuthenticationFailed('No refresh token.')

        try:
            refresh = RefreshToken(raw_refresh)
        except TokenError:
            raise AuthenticationFailed('Refresh token is invalid or expired.')

        response = Response({'message': 'Token refreshed.'}, status=status.HTTP_200_OK)
        response.set_cookie(
            key      = cookie_settings['ACCESS_COOKIE_NAME'],
            value    = str(refresh.access_token),
            max_age  = cookie_settings['ACCESS_MAX_AGE'],
            httponly = cookie_settings['HTTP_ONLY'],
            samesite = cookie_settings['SAMESITE'],
            secure   = cookie_settings['SECURE'],
        )
        return response


class DeliveryUsersView(APIView):
    """GET /api/auth/delivery-users/ — admin only, used to populate assign dropdown."""
    permission_classes = [IsAuthenticated, IsAdmin]

    @extend_schema(
        responses={200: UserResponseSerializer(many=True)},
        tags=['Auth'],
        summary='List all delivery users (admin only)',
    )
    def get(self, request):
        delivery_users = User.objects.filter(role=Role.DELIVERY)
        return Response(UserResponseSerializer(delivery_users, many=True).data, status=status.HTTP_200_OK)
