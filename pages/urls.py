from django.urls import path
from django.contrib.auth import views as auth_views

from pages.views import index, PasswordResetView, user_register, user_login, signout, home, book_detail, news, support, \
    account_setting, borrow_book, return_book, balance, order, manager_home

urlpatterns = [
    path("", index),
    path("accounts/password_reset/", PasswordResetView.as_view(), name="password_reset"),
    path("accounts/password_reset/done/", auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path("accounts/reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("accounts/register/", user_register, name="register"),
    path("accounts/login/", user_login, name="login"),
    path("accounts/login/", user_login, name="password_reset_complete"), # quick hack for redirection after password reset
    path("accounts/logout/", signout, name="signout"),
    path("home/", home, name="home"),
    path("support/", support, name="support"),
    path("news/", news, name="news"),
    path("account_setting/",account_setting, name="account_setting"),
    path("balance/", balance, name="balance"),
    path("order/", order, name="order"),
    path("books/", book_detail, name='book_detail'),
    path('books/<int:book_id>/borrow/', borrow_book, name='borrow_book'),  # Borrow book
    path('books/<int:book_id>/return/', return_book, name='return_book'),  # Return book
    path("home/manager_home",manager_home, name="manager_home")
]
