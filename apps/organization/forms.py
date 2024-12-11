from django import forms
from .models import Application,Organization

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



class OrganizationModelForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={}),required=True)
    address = forms.CharField(widget=forms.TextInput(attrs={}),required=False)
    city = forms.CharField(widget=forms.TextInput(attrs={}),required=False)
    phone = forms.CharField(widget=forms.TextInput(attrs={}),required=True)
    teamviewer = forms.CharField(widget=forms.TextInput(attrs={}),required=False)
    email = forms.CharField(widget=forms.TextInput(attrs={}),required=False)
    website = forms.CharField(widget=forms.TextInput(attrs={}),required=False)
    is_visible = forms.BooleanField(initial=True,widget=forms.CheckboxInput(attrs={'class': 'h-4 w-4 text-blue-600 border-gray-300 rounded',}),required=True)
    class Meta:
        model = Organization
        fields = ['name', 'address', 'city','phone','teamviewer','email','website','is_visible']