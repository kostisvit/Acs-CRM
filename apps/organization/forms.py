from django import forms
from .models import Application

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application  # Link the form to the Application model
        fields = ['title', 'description']  # Specify the fields to include in the form
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-input block w-full border-gray-300 rounded-md shadow-sm',
                'placeholder': 'Enter application name',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-textarea block w-full border-gray-300 rounded-md shadow-sm',
                'placeholder': 'Enter description (optional)',
                'rows': 1,
            }),
        }
