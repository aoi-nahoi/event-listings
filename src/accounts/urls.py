from __future__ import annotations

from django.urls import path

from . import views

app_name = "accounts"

urlpatterns = [
    path("register/", views.register_view, name="register"),
    path("login/", views.UserLoginView.as_view(), name="login"),
    path("logout/", views.UserLogoutView.as_view(), name="logout"),
    path("settings/", views.account_settings_view, name="settings"),
    path("password/change/", views.UserPasswordChangeView.as_view(), name="password_change"),
]
