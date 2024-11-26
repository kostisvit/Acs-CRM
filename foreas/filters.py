import django_filters
from .models import Dhmos
from django import forms


class PelatisFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='name',
        lookup_expr='icontains',
        label=False,
        widget=forms.TextInput(attrs={
            'class': 'block text-center sm:w-full md:w-1/3 py-2 border border-gray-300 text-gray-700 rounded-lg focus:ring-indigo-600 focus:border-indigo-600 sm:text-sm font-bold',  # Tailwind classes
            'placeholder': 'Φορέας...',
        }))
    phone = django_filters.CharFilter(field_name='phone',
        lookup_expr='icontains',
        label=False,
        widget=forms.TextInput(attrs={
            'class': 'block text-center sm:w-full md:w-1/3 py-2 border border-gray-300 text-gray-700 rounded-lg focus:ring-indigo-600 focus:border-indigo-600 sm:text-sm font-bold',  # Tailwind classes
            'placeholder': 'Τηλέφωνο...',
        }))
    email = django_filters.CharFilter(field_name='email',
        lookup_expr='icontains',
        label=False,
        widget=forms.TextInput(attrs={
            'class': 'block text-center sm:w-full md:w-1/3 py-2 border border-gray-300 text-gray-700 rounded-lg focus:ring-indigo-600 focus:border-indigo-600 sm:text-sm font-bold',  # Tailwind classes
            'placeholder': 'Email...',
        }))

    class Meta:
        model = Dhmos
        fields = ['name', 'phone','email']