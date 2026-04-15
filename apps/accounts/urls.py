from django.urls import path

from apps.accounts.views import RegisterView, LoginView, LogoutView, MeView, RefreshTokenView, DeliveryUsersView

urlpatterns = [
    path('register/',        RegisterView.as_view(),       name='auth-register'),
    path('login/',           LoginView.as_view(),          name='auth-login'),
    path('logout/',          LogoutView.as_view(),         name='auth-logout'),
    path('refresh/',         RefreshTokenView.as_view(),   name='auth-refresh'),
    path('me/',              MeView.as_view(),             name='auth-me'),
    path('delivery-users/',  DeliveryUsersView.as_view(),  name='auth-delivery-users'),
]
