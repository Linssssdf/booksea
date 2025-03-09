from django.urls import path
from django.contrib.auth import views as auth_views

from pages.views import index, PasswordResetView, user_register, user_login, signout, home

urlpatterns = [
    path("", index),
        path('accounts/password_reset/', PasswordResetView.as_view(), name='password_reset'),
        path('accounts/password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
        path('accounts/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
        path("accounts/register/", user_register, name="register"),
        path("accounts/login/", user_login, name="login"),
        path("accounts/login/", user_login, name="password_reset_complete"), # quick hack for redirection after password reset
        path("accounts/logout/", signout, name="signout"),
        path("home/", home, name="home"),
]
