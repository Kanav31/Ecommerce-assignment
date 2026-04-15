from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings


class CookieJWTAuthentication(JWTAuthentication):
    """Reads the JWT access token from an HttpOnly cookie instead of the Authorization header."""

    def authenticate(self, request):
        cookie_name = settings.JWT_COOKIE_SETTINGS['ACCESS_COOKIE_NAME']
        raw_token   = request.COOKIES.get(cookie_name)

        if raw_token is None:
            return None  # no cookie — anonymous request, not an error

        try:
            validated_token = self.get_validated_token(raw_token)
        except TokenError as e:
            raise AuthenticationFailed(str(e))

        try:
            user = self.get_user(validated_token)
        except InvalidToken as e:
            raise AuthenticationFailed(str(e))

        return (user, validated_token)
