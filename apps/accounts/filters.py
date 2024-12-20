import django_filters
from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Adeia
from .model_choices import *
from django.contrib.auth import get_user_model

User = get_user_model()

class AdeiaFilter(django_filters.FilterSet):
  acs_employee = django_filters.ModelChoiceFilter(
    queryset=User.objects.filter(is_active=True),
    label=False,
    empty_label="Επιλέξτε υπάλληλο",
    widget=forms.Select(attrs={
            'class': 'form-select text-center mt-1 block border border-gray-300 rounded-lg text-gray-700 font-medium py-2 sm:w-full md:w-1/3',  # Added 'py-2' and width classes for consistency
        })
        )
  adeiatype = django_filters.ChoiceFilter(choices=adeia_choice,
    label=False,
    empty_label="Επιλέξτε τύπο άδειας",
    widget=forms.Select(attrs={
            'class': 'form-select text-center mt-1 block border border-gray-300 rounded-lg text-gray-700 font-medium py-2 sm:w-full md:w-1/3',  # Added 'py-2' and width classes for consistency
        })
        )
  class Meta:
    model = Adeia
    fields = ['acs_employee','adeiatype']