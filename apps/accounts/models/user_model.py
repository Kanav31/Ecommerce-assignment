from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models

from apps.accounts.constants import Role
from apps.accounts.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model — uses email instead of username for authentication."""

    email = models.EmailField(unique=True)
    name  = models.CharField(max_length=150)
    role  = models.CharField(
        max_length=10,
        choices=Role.CHOICES,
        default=Role.CUSTOMER,
    )

    is_active = models.BooleanField(default=True)
    is_staff  = models.BooleanField(default=False)  # True = can access /admin/

    created_at = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD  = 'email'
    REQUIRED_FIELDS = ['name']

    class Meta:
        db_table = 'users'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.name} ({self.email})'
