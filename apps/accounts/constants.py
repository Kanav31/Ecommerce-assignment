from django.db import models

class Role(models.TextChoices):
    ADMIN = 'admin',    'Admin'
    CUSTOMER = 'customer', 'Customer'
    DELIVERY = 'delivery', 'Delivery Man'

class AuthMessage:
    # Success messages
    REGISTER_SUCCESS = 'Registered successfully.'
    LOGIN_SUCCESS = 'Logged in successfully.'
    LOGOUT_SUCCESS = 'Logged out successfully.'
    ME_SUCCESS = 'User fetched successfully.'
    TOKEN_REFRESHED = 'Token refreshed successfully.'
    DELIVERY_USERS_FETCH = 'Delivery users fetched successfully.'

    # Error messages
    INVALID_CREDENTIALS = 'Invalid email or password.'
    REFRESH_TOKEN_REQUIRED = 'refresh_token is required.'
    REFRESH_TOKEN_INVALID = 'Refresh token is invalid or expired.'
    EMAIL_ALREADY_EXISTS = 'A user with this email already exists.'
