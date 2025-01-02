from django import forms
from django.forms import ModelChoiceField
from .models import Application,Organization, Ergasies, Employee, Department
from accounts.models import User
from django.core.exceptions import ValidationError


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


class OrganizationForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'class': 'block w-full px-4 py-2 border rounded-lg text-gray-700'}),required=True)
    address = forms.CharField(widget=forms.TextInput(attrs={'class': 'block w-full px-4 py-2 border rounded-lg text-gray-700'}),required=False)
    city = forms.CharField(widget=forms.TextInput(attrs={'class': 'block w-full px-4 py-2 border rounded-lg text-gray-700'}),required=False)
    phone = forms.CharField(widget=forms.TextInput(attrs={'class': 'block w-full px-4 py-2 border rounded-lg text-gray-700'}),required=True)
    teamviewer = forms.CharField(widget=forms.TextInput(attrs={'class': 'block w-full px-4 py-2 border rounded-lg text-gray-700'}),required=False)
    email = forms.CharField(widget=forms.TextInput(attrs={'class': 'block w-full px-4 py-2 border rounded-lg text-gray-700'}),required=False)
    website = forms.URLField(widget=forms.TextInput(attrs={'class': 'block w-full px-4 py-2 border rounded-lg text-gray-700','placeholder':'https://www.example.com'}),required=False)
    is_visible = forms.BooleanField(initial=True,widget=forms.CheckboxInput(attrs={'class': 'h-4 w-4 text-blue-600 border-gray-300 rounded',}),required=False)
    class Meta:
        model = Organization
        fields = ['name', 'address', 'city','phone','teamviewer','email','website','is_visible']


class OrgEmployeeForm(forms.ModelForm):
    organization = ModelChoiceField(queryset=Organization.objects.filter(is_visible=True),
        widget=forms.Select(attrs={'class': 'mt-1 block w-full  rounded-md shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-500 focus:ring-opacity-50 text-gray-700'}),
        label='Μαθητής',
        required=True)
    firstname = forms.CharField(widget=forms.TextInput(attrs={'class': 'block w-full px-4 py-2 border rounded-lg text-gray-700'}),required=True)
    lastname = forms.CharField(widget=forms.TextInput(attrs={'class': 'block w-full px-4 py-2 border rounded-lg text-gray-700'}),required=True)
    department = ModelChoiceField(queryset=Department.objects.all(),
        widget=forms.Select(attrs={'class': 'mt-1 block w-full  rounded-md shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-500 focus:ring-opacity-50 text-gray-700'}),
        label='Υπηρεσία',
        required=False)
    phone = forms.CharField(widget=forms.TextInput(attrs={'class': 'block w-full px-4 py-2 border rounded-lg text-gray-700'}),required=False)
    cellphone = forms.CharField(widget=forms.TextInput(attrs={'class': 'block w-full px-4 py-2 border rounded-lg text-gray-700'}),required=False)
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'block w-full px-4 py-2 border rounded-lg text-gray-700'}),required=False)
    secondary_email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'block w-full px-4 py-2 border rounded-lg text-gray-700'}),required=False)
    info = forms.CharField(widget=forms.Textarea(attrs={'class': 'block w-full px-4 py-2 border rounded-lg text-gray-700'}),required=False)
    is_visible = forms.BooleanField(initial=True,widget=forms.CheckboxInput(attrs={'class': 'h-4 w-4 text-blue-600 border-gray-300 rounded',}),required=False)
    
    class Meta:
        model = Employee
        fields = ['organization','firstname','lastname','department','phone','cellphone','email','secondary_email','info','is_visible']
    


class TaskForm(forms.ModelForm):
    organization = ModelChoiceField(queryset=Organization.objects.filter(is_visible=True),
        widget=forms.Select(attrs={'class': 'mt-1 block w-full  rounded-md shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-500 focus:ring-opacity-50 text-gray-700'}),
        label='Μαθητής',
        required=True)
    importdate = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date','class': 'block w-full rounded-md mt-1   text-gray-700 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6','placeholder': 'YYYY-MM-DD',}),
        required=True)
    app = forms.ModelChoiceField(queryset=Application.objects.all(),
        widget=forms.Select(attrs={'class': 'mt-1 block w-full  rounded-md shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-500 focus:ring-opacity-50 text-gray-700'}),
        label='Εφαρμογή',
        required=True)
    info = forms.CharField(widget=forms.Textarea(attrs={'class': 'block w-full px-4 py-2 border rounded-lg text-gray-700'}),required=True)
    text = forms.CharField(widget=forms.Textarea(attrs={'class': 'block w-full px-4 py-2 border rounded-lg text-gray-700'}),required=False)
    time = forms.FloatField(widget=forms.NumberInput(attrs={'class': 'block w-full mt-1 px-4 py-2 border rounded-lg text-gray-700'}),required=False)
    employee = ModelChoiceField(queryset=User.objects.all(),
        widget=forms.Select(attrs={'class': 'mt-1 block w-full  rounded-md shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-500 focus:ring-opacity-50 text-gray-700'}),
        label='ACS',
        required=True)
    org_employee = ModelChoiceField(queryset=Employee.objects.filter(is_visible=True),widget=forms.Select(attrs={'class': 'mt-1 block w-full  rounded-md shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-500 focus:ring-opacity-50 text-gray-700'}),
        label='ACS',
        required=True)
    class Meta:
        model = Ergasies
        fields = ['organization','importdate','app','jobtype','info','text','time','employee']
        widgets = {
            'jobtype': forms.Select(attrs={'class': 'block w-full px-4 py-2 border rounded-lg'}),
        }