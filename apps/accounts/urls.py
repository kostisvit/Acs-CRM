from django.contrib.auth import views as auth_views
from django.urls import path, reverse_lazy

from apps.accounts.export import export_adeia

from .views import FirstPasswordChangeView, MyLeaveListView, login_view, logout_view, profile, users_view

app_name = "accounts"

urlpatterns = [
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("users/", users_view, name="users"),
    path(
        "my-leaves/",
        MyLeaveListView.as_view(),
        name="my_leave_dashboard"
    ),
    path("profile/", profile, name="profile"),
    path(
        "export-my-leaves/",
        export_adeia,
        name="export_my_leaves"
    ),
    path("change-password/", FirstPasswordChangeView.as_view(),
         name="change_password",),

    path(
        "password-reset/",
        auth_views.PasswordResetView.as_view(
            template_name="registration/password_reset_form.html",
            email_template_name="registration/password_reset_email.html",
            subject_template_name="registration/password_reset_subject.txt",
            success_url=reverse_lazy("accounts:password_reset_done"),
        ),
        name="password_reset",
    ),
    path(
        "password-reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="registration/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="registration/password_reset_confirm.html",
            success_url="/reset/done/",
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="registration/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
]
