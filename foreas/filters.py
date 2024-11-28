import django_filters
from .models import Dhmos, Employee
from django import forms
from django.utils.translation import gettext_lazy as _


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


class EpafiFilter(django_filters.FilterSet):
    dhmos = django_filters.ModelChoiceFilter(queryset=Dhmos.objects.filter(is_visible=True),
        label=False,
        empty_label="Επιλέξτε Οργανισμό...",
        widget=forms.Select(attrs={
            'class': 'form-select text-center mt-1 block border border-gray-300 rounded-lg text-gray-700 font-medium',
        }))
    firstname = django_filters.CharFilter(
        lookup_expr='icontains', 
        label=False,
        widget=forms.TextInput(attrs={
            'class': 'block text-center sm:w-full md:w-1/3 py-2 border border-gray-300 text-gray-700 rounded-lg focus:ring-indigo-600 focus:border-indigo-600 sm:text-sm font-bold',  # Tailwind classes
            'placeholder': 'Όνομα...',
        }))
    lastname = django_filters.CharFilter(
        lookup_expr='icontains', 
        label=False,
        widget=forms.TextInput(attrs={
            'class': 'block text-center sm:w-full md:w-1/3 py-2 border border-gray-300 text-gray-700 rounded-lg focus:ring-indigo-600 focus:border-indigo-600 sm:text-sm font-bold',  # Tailwind classes
            'placeholder': 'Επώνυμο...',
        }))

    class Meta:
        model = Employee
        fields = ['dhmos', 'firstname', 'lastname']

    def __init__(self, *args, **kwargs):
        super(EpafiFilter, self).__init__(*args, **kwargs)
        if self.data == {}:
            self.queryset = self.queryset.none()