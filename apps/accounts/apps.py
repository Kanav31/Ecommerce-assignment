from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    # Full dotted path because the app lives inside apps/ directory
    name = 'apps.accounts'
