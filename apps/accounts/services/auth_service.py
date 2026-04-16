from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from apps.accounts.constants import AuthMessage
from apps.accounts.models import User


class AuthService:
    @staticmethod
    def register_user(validated_data: dict) -> User:
        return User.objects.create_user(
            email = validated_data['email'],
            password = validated_data['password'],
            name = validated_data['name'],
            role = validated_data.get('role', 'customer'),
        )

    @staticmethod
    def login_user(email: str, password: str) -> User:
        user = authenticate(username=email, password=password)
        if user is None:
            raise AuthenticationFailed(AuthMessage.INVALID_CREDENTIALS)
        return user

    @staticmethod
    def generate_tokens(user: User) -> dict:
        refresh = RefreshToken.for_user(user)
        return {
            'access_token':  str(refresh.access_token),
            'refresh_token': str(refresh),
        }

    @staticmethod
    def refresh_tokens(raw_refresh: str) -> dict:
        if not raw_refresh:
            raise AuthenticationFailed(AuthMessage.REFRESH_TOKEN_REQUIRED)
        try:
            refresh = RefreshToken(raw_refresh)
            # Rotate: new JTI + expiry invalidates the old refresh token
            refresh.set_jti()
            refresh.set_exp()
        except TokenError:
            raise AuthenticationFailed(AuthMessage.REFRESH_TOKEN_INVALID)
        return {
            'access_token':  str(refresh.access_token),
            'refresh_token': str(refresh),
        }
