import django_filters
from django.contrib.auth import get_user_model
from django.db.models import Q

from .models import Customer

User = get_user_model()

class CustomerFilter(django_filters.FilterSet):

    customer = django_filters.ModelChoiceFilter(
        queryset=Customer.objects.filter(
            is_active=True,
        ).order_by("lastname", "firstname"),
        empty_label="Πελάτης",
    )


    def filter_search(self, queryset, name, value):
        if not value:
            return queryset

        return queryset.filter(
            Q(company_name__icontains=value)
            | Q(company_email__icontains=value)
            | Q(phone_icontains=value)
        )

    class Meta:
        model = Customer
        fields = [
            "customer",
            "q",
        ]
