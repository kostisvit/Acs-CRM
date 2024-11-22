# accounts/forms.py

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError


UserModel = get_user_model()

# Email authentication, check email if exists
class EmailAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label="Email", max_length=254, widget=forms.EmailInput(attrs={'autofocus': True}))

    def clean_username(self):
        email = self.cleaned_data.get('username')
        if not UserModel.objects.filter(email=email).exists():
            raise ValidationError("Το email δεν υπάρχει, επικοινωνήστε με τον διαχειριστή. ")
        return email
