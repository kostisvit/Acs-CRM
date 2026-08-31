from .models import Adeia
from typing import Any, ClassVar

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordChangeForm

User = get_user_model()


INPUT_CLASS = (
    "block w-full rounded-lg border border-gray-300 bg-white px-3 py-2 "
    "text-sm shadow-sm placeholder:text-gray-400 "
    "focus:border-teal-300 focus:ring-2 focus:ring-teal-400 focus:outline-none"
)


class EmailLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)


class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Change labels
        self.fields["old_password"].label = "Τρέχον Κωδικός"
        self.fields["new_password1"].label = "Νέος Κωδικός"
        self.fields["new_password2"].label = "Επιβεβαίωση Κωδικού"

        for field in self.fields.values():
            field.widget.attrs.update(
                {
                    "class": (
                        "w-full px-4 py-3 border border-gray-300 "
                        "rounded-lg focus:ring-2 focus:ring-teal-500 "
                        "focus:border-teal-700 outline-none"
                    )
                }
            )


class UserProfileForm(forms.ModelForm):

    class Meta:
        model = User

        fields: ClassVar[list[str]] = [
            "first_name",
            "last_name",
            "email",
            "allowed_leave_days",
        ]

        labels = {
            "first_name": "Όνομα",
            "last_name": "Επώνυμο",
            "allowed_leave_days": "Επιτρεπόμενες Μέρες Αδείας συν υπόλοιπο",
            "email": "Διεύθυνση Email",
        }

        widgets: ClassVar[dict[str, Any]] = {
            "first_name": forms.TextInput(
                attrs={
                    "class": (
                        "w-full px-4 py-3 border border-gray-300 "
                        "rounded-lg focus:ring-2 focus:ring-teal-500 "
                        "focus:border-teal-700 outline-none"
                    )
                }
            ),
            "last_name": forms.TextInput(
                attrs={
                    "class": "w-full px-4 py-3 border border-gray-300 "
                    "rounded-lg focus:ring-2 focus:ring-teal-500 "
                    "focus:border-teal-700 outline-none"
                }
            ),
            "allowed_leave_days": forms.NumberInput(
                attrs={
                    "class": "w-full px-4 py-3 border border-gray-300 "
                    "rounded-lg focus:ring-2 focus:ring-teal-500 "
                    "focus:border-teal-700 outline-none",
                    "min": "0",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": "w-full px-4 py-3 border border-gray-300 "
                    "rounded-lg focus:ring-2 focus:ring-teal-500 "
                    "focus:border-teal-700 outline-none",
                }
            ),
        }


class AdeiaForm(forms.ModelForm):
    class Meta:
        model = Adeia
        fields = [
            "acs_employee",
            "acs_adeiatype",
            "startdate",
            "enddate",
        ]
        widgets = {
            "acs_employee": forms.Select(
                attrs={"class": INPUT_CLASS}
            ),
            "acs_adeiatype": forms.Select(
                attrs={"class": INPUT_CLASS}
            ),
            "startdate": forms.DateInput(
                attrs={
                    "class": INPUT_CLASS + " flatpickr",
                    "autocomplete": "off",
                },
            ),
            "enddate": forms.DateInput(
                attrs={
                    "class": INPUT_CLASS + " flatpickr",
                    "autocomplete": "off",
                },
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["acs_employee"].queryset = User.objects.filter(
            is_active=True, groups__name="employee"
        )

    def clean(self):
        cleaned_data = super().clean()

        startdate = cleaned_data.get("startdate")
        enddate = cleaned_data.get("enddate")

        if startdate and enddate and enddate < startdate:
            raise forms.ValidationError(
                "Η ημερομηνία λήξης δεν μπορεί να είναι πριν "
                "από την ημερομηνία έναρξης."
            )

        return cleaned_data
