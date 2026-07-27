from __future__ import annotations

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy

from .forms import RegisterForm


def register_view(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        return redirect("events:event_list")

    form = RegisterForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, "Account created. You are now logged in.")
        return redirect("events:event_list")
    return render(request, "accounts/register.html", {"form": form})


class UserLoginView(LoginView):
    template_name = "accounts/login.html"
    redirect_authenticated_user = True


class UserLogoutView(LogoutView):
    next_page = reverse_lazy("events:event_list")
