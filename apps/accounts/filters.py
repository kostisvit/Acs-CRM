import django_filters
from django.contrib.auth import get_user_model

from apps.accounts.models import Adeia

User = get_user_model()

# Το χρησιμοποιούμε για να φιλτράρουμε τις άδειες που έχει πάρει ένας υπάλληλος.


class DayOffFilter(django_filters.FilterSet):
    acs_employee = django_filters.ModelChoiceFilter(
        queryset=User.objects.filter(is_active=True), label="Υπάλληλος")

    class Meta:
        model = Adeia
        fields = ["acs_employee", "startdate", "enddate",]
