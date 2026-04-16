from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from drf_spectacular.utils import extend_schema
from apps.accounts.constants import AuthMessage, Role
from apps.accounts.models import User
from apps.accounts.permissions import IsAdmin
from apps.accounts.serializers import (
    RegisterRequestSerializer,
    LoginRequestSerializer,
    UserResponseSerializer,
)
from apps.accounts.services import AuthService
from core.response import success_response

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
        return success_response(
            message = AuthMessage.REGISTER_SUCCESS,
            status_code = 201,
            data = UserResponseSerializer(user).data,
        )

class LoginView(APIView):
    """POST /api/auth/login/ — returns access + refresh tokens in the response body."""
    permission_classes = [AllowAny]
    @extend_schema(
        request=LoginRequestSerializer,
        responses={200: UserResponseSerializer},
        tags=['Auth'],
        summary='Login and receive JWT tokens',
    )
    def post(self, request):
        serializer = LoginRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = AuthService.login_user(
            email = serializer.validated_data['email'],
            password = serializer.validated_data['password'],
        )
        tokens = AuthService.generate_tokens(user)
        return success_response(
            message = AuthMessage.LOGIN_SUCCESS,
            data = {**UserResponseSerializer(user).data, **tokens},
        )

class LogoutView(APIView):
    """
    POST /api/auth/logout/
    Token is stateless — client deletes it from localStorage.
    This endpoint exists so the frontend has a clean logout call to make.
    """
    permission_classes = [IsAuthenticated]
    @extend_schema(request=None, responses={200: None}, tags=['Auth'], summary='Logout')
    def post(self, request):
        return success_response(message=AuthMessage.LOGOUT_SUCCESS)

class MeView(APIView):
    """GET /api/auth/me/"""
    permission_classes = [IsAuthenticated]
    @extend_schema(
        responses={200: UserResponseSerializer},
        tags=['Auth'],
        summary='Get current authenticated user',
    )
    def get(self, request):
        return success_response(
            message = AuthMessage.ME_SUCCESS,
            data = UserResponseSerializer(request.user).data,
        )

class RefreshTokenView(APIView):
    """POST /api/auth/refresh/ — body: { refresh_token: '...' }"""
    permission_classes = [AllowAny]
    @extend_schema(request=None, responses={200: None}, tags=['Auth'], summary='Refresh access token')
    def post(self, request):
        tokens = AuthService.refresh_tokens(request.data.get('refresh_token'))
        return success_response(message=AuthMessage.TOKEN_REFRESHED, data=tokens)


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
        return success_response(
            message = AuthMessage.DELIVERY_USERS_FETCH,
            data = UserResponseSerializer(delivery_users, many=True).data,
        )
