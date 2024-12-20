import django_filters
from django.contrib.auth import get_user_model
from .models import Organization, Employee, Ergasies,Application
from django import forms
from django.utils.translation import gettext_lazy as _
from .model_choices import *


User = get_user_model()

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
        model = Organization
        fields = ['name', 'phone','email']


class EpafiFilter(django_filters.FilterSet):
    IS_ACTIVE_CHOICES = (
        (True, 'Online'),
        (False, 'Offline'),
    )
    
    organization = django_filters.ModelChoiceFilter(
        queryset=Organization.objects.filter(is_visible=True),
        label=False,
        empty_label="Επιλέξτε Οργανισμό...",
        widget=forms.Select(attrs={
            'class': 'form-select text-center mt-1 block border border-gray-300 rounded-lg text-gray-700 font-medium py-2 sm:w-full md:w-1/3',  # Added 'py-2' and width classes for consistency
        })
    )
    firstname = django_filters.CharFilter(
        lookup_expr='icontains', 
        label=False,
        widget=forms.TextInput(attrs={
            'class': 'block text-center mt-1 block border border-gray-300 rounded-lg text-gray-700 font-medium py-2 sm:w-full md:w-1/3',  # Matches dhmos widget
            'placeholder': 'Όνομα...',
        })
)
    lastname = django_filters.CharFilter(
        lookup_expr='icontains', 
        label=False,
        widget=forms.TextInput(attrs={
            'class': 'block text-center mt-1 block border border-gray-300 rounded-lg text-gray-700 font-medium py-2 sm:w-full md:w-1/3',  # Tailwind classes
            'placeholder': 'Επώνυμο...',
        }))
    is_visible = django_filters.ChoiceFilter(field_name='is_visible',
        empty_label="Κατάσταση...",
        label=False,
        choices=IS_ACTIVE_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-select sm:w-full md:w-1/3 text-center mt-1 block  border border-gray-300 rounded-lg text-gray-700 font-medium',
        }))

    class Meta:
        model = Employee
        fields = ['organization', 'firstname', 'lastname']

    def __init__(self, *args, **kwargs):
        super(EpafiFilter, self).__init__(*args, **kwargs)
        if self.data == {}:
            self.queryset = self.queryset.none()


class TaskFilter(django_filters.FilterSet):
    
    organization = django_filters.ModelChoiceFilter(
        queryset=Organization.objects.filter(is_visible=True),
        label=False,
        empty_label="Επιλέξτε Οργανισμό...",
        widget=forms.Select(attrs={
            'class': 'form-select text-center mt-1 block border border-gray-300 rounded-lg text-gray-700 font-medium py-2 sm:w-full md:w-1/3',  # Added 'py-2' and width classes for consistency
        })
    )
    jobtype = django_filters.ChoiceFilter(
        choices=job_choice,
        label=False,
        empty_label="Τύπος εργασίας...",
        widget=forms.Select(attrs={
            'class': 'form-select text-center mt-1 block border border-gray-300 rounded-lg text-gray-700 font-medium py-2 lg:w-44 ',
        }))
    app = django_filters.ModelChoiceFilter(
        queryset=Application.objects.filter(is_active=True),
        label=False,
        empty_label="Επιλέξτε Εφαρμογή...",
        widget=forms.Select(attrs={
            'class': 'form-select text-center mt-1 block border border-gray-300 rounded-lg text-gray-700 font-medium py-2 sm:w-full  md:w-1/3',  # Added 'py-2' and width classes for consistency
        })
    )
    employee = django_filters.ModelChoiceFilter(        
        queryset=User.objects.filter(is_active=True),
        label=False,
        empty_label="Επιλέξτε Υπάλληλο...",
        widget=forms.Select(attrs={
            'class': 'form-select text-center mt-1 block border border-gray-300 rounded-lg text-gray-700 font-medium py-2 sm:w-full  md:w-1/3',  # Added 'py-2' and width classes for consistency
        })
    )
    importdate = django_filters.DateFromToRangeFilter(
        label=False,
        widget=django_filters.widgets.RangeWidget(
            attrs={
                'placeholder': 'dd/mm/yyyy',
                'type': 'date',
                'class': 'form-input text-center mt-1 border border-gray-300 rounded-lg text-gray-700 font-medium py-2 inline-block mr-2',  # Smaller width and inline-block for horizontal alignment  # Tailwind form styles
            }
        )
    )
    
    class Meta:
        model = Ergasies
        fields = ['organization', 'app', 'employee', 'jobtype', 'importdate']

    def __init__(self, *args, **kwargs):
        super(TaskFilter, self).__init__(*args, **kwargs)
        if self.data == {}:
            self.queryset = self.queryset.none()