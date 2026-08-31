import django_filters
from django_filters.widgets import RangeWidget
from .models import Organization, Task
from apps.parameters.models import JobType, OtsSoftware
from django.contrib.auth import get_user_model

User = get_user_model()


# Χρησιμοποιείται κατά την εξαγωγή των εργασιών σε Excel, για να φιλτράρει τα αποτελέσματα
class ErgasiaFilter(django_filters.FilterSet):
    organization = django_filters.ModelChoiceFilter(
        queryset=Organization.objects.filter(is_active=True), empty_label="Επιλέξτε Οργανισμό"
    )
    job_type_acs = django_filters.ModelChoiceFilter(
        queryset=JobType.objects.filter(is_active=True), empty_label="Επιλέξτε Εργασία"
    )
    org_app = django_filters.ModelChoiceFilter(
        queryset=OtsSoftware.objects.filter(is_active=True), empty_label="Επιλέξτε Εφαρμογή"
    )
    acs_employee = django_filters.ModelChoiceFilter(
        queryset=User.objects.filter(
            is_active=True).order_by("last_name"),
        empty_label="Υπάλληλος ACS",
    )
    importdate = django_filters.DateFromToRangeFilter(
        label="Ημ. Καταχώρησης",
        widget=RangeWidget(
            attrs={
                "class": "daterange-widget",
                "placeholder": "dd/mm/yyyy",
                "type": "date",
            }
        ),
    )
    year = django_filters.NumberFilter(
        field_name="importdate", lookup_expr="year", label="Έτος")

    class Meta:
        model = Task
        fields = ["organization", "org_app", "acs_employee",
                  "job_type_acs", "importdate", "year"]
