from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import CustomUser, Adeia
from django import forms

class CustomUserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = CustomUser
        fields = "__all__"


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser

    fieldsets = (
        (None, {
            "fields": ("email", 
                        "password",
                        "first_name",
                        "last_name",)
        }),
        ("Permissions", {
            "fields": (
                "is_active",
                "is_staff",
                "is_superuser",
                "must_change_password",
                "groups",
                "user_permissions",
            )
        }),
        ("Important dates", {
            "fields": (
                "last_login",
            )
        }),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email",
                "password1",
                "password2",
                "is_active",
                "is_staff",
                "must_change_password",
            ),
        }),
    )

    list_display = (
        "email",
        "is_staff",
        "is_active",
    )

    ordering = ("email",)

    @admin.register(Adeia)
    class AdeiaAdmin(admin.ModelAdmin):
        model = Adeia
        list_display = ["acs_employee","acs_adeiatype", "startdate","enddate","source_id"]