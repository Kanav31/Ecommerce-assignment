from rest_framework import serializers
from apps.accounts.constants import AuthMessage, Role
from apps.accounts.models import User


class RegisterRequestSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(min_length=8, write_only=True)
    role = serializers.ChoiceField(choices=Role.choices, default=Role.CUSTOMER)

    def validate_email(self, value):
        if User.objects.filter(email=value.lower()).exists():
            raise serializers.ValidationError(AuthMessage.EMAIL_ALREADY_EXISTS)
        return value.lower()
