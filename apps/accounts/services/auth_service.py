from django.conf import settings
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken

from apps.accounts.models import User


class AuthService:

    @staticmethod
    def register_user(validated_data: dict) -> User:
        return User.objects.create_user(
            email    = validated_data['email'],
            password = validated_data['password'],
            name     = validated_data['name'],
            role     = validated_data.get('role', 'customer'),
        )

    @staticmethod
    def login_user(email: str, password: str) -> User:
        user = authenticate(username=email, password=password)
        if user is None:
            raise AuthenticationFailed('Invalid email or password.')
        return user

    @staticmethod
    def set_jwt_cookies(response, user: User) -> None:
        cookie_settings = settings.JWT_COOKIE_SETTINGS

        refresh       = RefreshToken.for_user(user)
        access_token  = str(refresh.access_token)
        refresh_token = str(refresh)

        response.set_cookie(
            key      = cookie_settings['ACCESS_COOKIE_NAME'],
            value    = access_token,
            max_age  = cookie_settings['ACCESS_MAX_AGE'],
            httponly = cookie_settings['HTTP_ONLY'],
            samesite = cookie_settings['SAMESITE'],
            secure   = cookie_settings['SECURE'],
        )

        response.set_cookie(
            key      = cookie_settings['REFRESH_COOKIE_NAME'],
            value    = refresh_token,
            max_age  = cookie_settings['REFRESH_MAX_AGE'],
            httponly = cookie_settings['HTTP_ONLY'],
            samesite = cookie_settings['SAMESITE'],
            secure   = cookie_settings['SECURE'],
        )

    @staticmethod
    def get_cookie_settings() -> dict:
        return settings.JWT_COOKIE_SETTINGS

    @staticmethod
    def clear_jwt_cookies(response) -> None:
        cookie_settings = settings.JWT_COOKIE_SETTINGS
        response.delete_cookie(cookie_settings['ACCESS_COOKIE_NAME'])
        response.delete_cookie(cookie_settings['REFRESH_COOKIE_NAME'])
