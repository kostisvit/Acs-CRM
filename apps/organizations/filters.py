
import django_filters
from django.contrib.auth import get_user_model
from django.db.models import Q

from apps.parameters.models import JobType, OtsSoftware

from .models import (
    Employee,
    Organization,
    Task,
)

User = get_user_model()


class ErgasiaFilter(django_filters.FilterSet):

    organization = django_filters.ModelChoiceFilter(
        queryset=Organization.objects.filter(is_active=True),
        empty_label="Επιλέξτε Οργανισμό",
    )

    job_type_acs = django_filters.ModelChoiceFilter(
        queryset=JobType.objects.filter(is_active=True),
        empty_label="Επιλέξτε Εργασία",
    )

    org_app = django_filters.ModelChoiceFilter(
        queryset=OtsSoftware.objects.filter(is_active=True),
        empty_label="Επιλέξτε Εφαρμογή",
    )

    acs_employee = django_filters.ModelChoiceFilter(
        queryset=User.objects.filter(
            is_active=True,
            groups__name="employee",
        )
        .distinct()
        .order_by("last_name", "first_name"),
        empty_label="Υπάλληλος ACS",
    )

    org_employee = django_filters.ModelChoiceFilter(
        queryset=Employee.objects.filter(
            is_active=True,
        ).order_by("lastname", "firstname"),
        empty_label="Υπάλληλος Οργανισμού",
    )

    ticketid = django_filters.CharFilter(
        field_name="ticketid",
        lookup_expr="icontains",
        label="Ticket ID",
    )

    importdate = django_filters.DateFromToRangeFilter(
        label="Ημ. Καταχώρησης",
    )

    year = django_filters.NumberFilter(
        field_name="importdate",
        lookup_expr="year",
        label="Έτος",
    )

    q = django_filters.CharFilter(
        method="filter_search",
        label="Αναζήτηση",
    )

    def filter_search(self, queryset, name, value):
        if not value:
            return queryset

        return queryset.filter(
            Q(task_info__icontains=value)
            | Q(task_note__icontains=value)
            | Q(ticketid__icontains=value)
        )

    class Meta:
        model = Task
        fields = [
            "organization",
            "org_app",
            "job_type_acs",
            "acs_employee",
            "org_employee",
            "ticketid",
            "importdate",
            "year",
            "q",
        ]
