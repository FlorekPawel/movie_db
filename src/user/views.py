from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import RegistrationForm
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
from django.contrib.messages.views import SuccessMessageMixin
from .models import Bookmark, Rating


def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Login successful.")
            return redirect("home")
        else:
            messages.success(request, "Wrong username or password.")
            return redirect("login")

    else:
        return render(request, "registration/login.html", {})


def logout_user(request):
    logout(request)
    messages.success(request, "You were logged out.")
    return redirect("home")


def register_user(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("home")
    else:
        form = RegistrationForm()
    return render(request, "authenticate/register.html", {"form": form})


def profile(request):
    bookmarks = Bookmark.objects.filter(user=request.user).values_list("movie_id", flat=True)
    ratings = Rating.objects.filter(user=request.user)
    
    star_range = range(5)
    return render(
        request,
        "profile.html",
        {
            "user": request.user,
            "bookmarks": bookmarks,
            "ratings": ratings,
            "star_range": star_range,
        },
    )


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = "password_reset_confirm.html"
    email_template_name = "password_reset_email.html"
    success_message = "We've emailed you instructions for setting your password."
    success_url = reverse_lazy("home")


class CustomPasswordResetConfirmView(PasswordResetConfirmView, SuccessMessageMixin):
    template_name = "password_reset_confirm.html"
    success_message = "Password has been changed."
    success_url = reverse_lazy("home")


def custom_success_page(request):
    return render(request, "password_reset_complete_custom.html")
