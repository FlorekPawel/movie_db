from django.urls import path
from . import views


urlpatterns = [
    path("profile", views.profile, name="profile"),
    path("login", views.login_user, name="login"),
    path("register_user", views.register_user, name="register"),
    path("password_reset", views.ResetPasswordView.as_view(), name="password_reset"),
    path("logout_user", views.logout_user, name="logout"),
    path(
        "reset/<uidb64>/<token>/",
        views.CustomPasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path("reset-success/", views.custom_success_page, name="custom_success_page"),
]
