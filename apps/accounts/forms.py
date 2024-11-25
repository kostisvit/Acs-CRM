# accounts/forms.py
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from django.forms import ModelChoiceField
from organization.models import Organization
from .choices import gender_choice
from django.contrib.auth.forms import UserCreationForm


UserModel = get_user_model()

# Email authentication, check email if exists
class EmailAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label="Email", max_length=254, widget=forms.EmailInput(attrs={'autofocus': True}))

    def clean_username(self):
        email = self.cleaned_data.get('username')
        if not UserModel.objects.filter(email=email).exists():
            raise ValidationError("Το email δεν υπάρχει, επικοινωνήστε με τον διαχειριστή. ")
        return email


# Custom user create form with default password
class UserCreationForm(forms.ModelForm):
    organization = ModelChoiceField(queryset=Organization.objects.all(),empty_label='Επιλέξτε οργανισμό...',widget=forms.Select(attrs={'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-500 focus:ring-opacity-50 text-gray-700'}),label='Οργανισμός',required=True)
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date','class': 'block w-full rounded-md border-0 py-1.5 text-gray-700 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-700 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6','placeholder': 'YYYY-MM-DD',}),label='Ημ. Γέννησης',required=False)
    gender = forms.ChoiceField(choices=gender_choice,widget=forms.Select(attrs={'class': 'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-500 focus:ring-opacity-50 text-gray-700'}),label='Φύλο',required=True)
    first_name = forms.CharField(label='Όνομα', widget=forms.TextInput(attrs={'class':'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-500 focus:ring-opacity-50 text-gray-700'}),required=True)
    last_name = forms.CharField(label='Επώνυμο',widget=forms.TextInput(attrs={'class':'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-500 focus:ring-opacity-50 text-gray-700'}),required=True)
    phone_number = forms.CharField(label='Τηλ. Επικ.',widget=forms.TextInput(attrs={'class':'block w-full rounded-md border-0 py-1.5 text-gray-700 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6'}),required=True)
    address = forms.CharField(label='Διεύθυνση',widget=forms.TextInput(attrs={'class':'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-500 focus:ring-opacity-50 text-gray-700'}),required=True)
    city = forms.CharField(label='Πόλη',widget=forms.TextInput(attrs={'class':'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-500 focus:ring-opacity-50 text-gray-700'}),required=False)
    country = forms.CharField(label='Χώρα',initial='Ελλάδα',widget=forms.TextInput(attrs={'class':'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-500 focus:ring-opacity-50 text-gray-700'}),required=False)
    postal_code = forms.CharField(label='ΤΚ',widget=forms.TextInput(attrs={'class':'mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-500 focus:ring-opacity-50 text-gray-700' }),required=False)
    is_active = forms.BooleanField(label='Κατάσταση',widget=forms.CheckboxInput(attrs={'class': 'h-4 w-4 text-blue-600 border-gray-300 rounded',}), initial=True,required=False)
    email = forms.EmailField(widget=forms.EmailInput(attrs={'autocomplete': 'off','class':'block w-full rounded-md border-0 py-1.5 text-gray-700 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6'}),required=True)
    is_staff = forms.BooleanField(initial=True,label='Καθηγητής',widget=forms.CheckboxInput(attrs={'class': 'h-4 w-4 text-blue-600 border-gray-300 rounded',}),required=False)
    is_company_owner = forms.BooleanField(label='Ιδιοκτήτης', initial=False, widget=forms.CheckboxInput(attrs={'class': 'h-4 w-4 text-blue-600 border-gray-300 rounded',}),required=False)
    is_student = forms.BooleanField(initial=False,label='Μαθητής',widget=forms.CheckboxInput(attrs={'class': 'h-4 w-4 text-blue-600 border-gray-300 rounded',}),required=False)
  
    
    
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('organization','email','first_name','last_name','date_of_birth','phone_number','address','city','postal_code','country','gender','is_active','is_staff','is_company_owner','is_student')

    
    def __init__(self, *args, **kwargs):
        # Capture the user from the form arguments
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # Ensure password fields are initialized
        if 'password1' not in self.fields:
            self.fields['password1'] = forms.CharField(widget=forms.PasswordInput(), required=False)
        if 'password2' not in self.fields:
            self.fields['password2'] = forms.CharField(widget=forms.PasswordInput(), required=False)

        # Filter courses based on user type
        # if user and user.is_superuser:
        #     # Superuser: Show all online courses
        #     self.fields['courses'].queryset = Course.objects.filter(is_online=True)
        # elif user and hasattr(user, 'organization'):
        #     # Regular user: Show only courses that are online and belong to the user's organization
        #     self.fields['courses'].queryset = Course.objects.filter(is_online=True, organization=user.organization)


    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password('password')  # Set your default password here
        # if commit:
        #     user.save()
        #     is_student = self.cleaned_data.get('is_student')
        #     student, created = Student.objects.get_or_create(user=user, defaults={'is_student': is_student})
            
        #     if not created:
        #         # Update is_student if Member already exists
        #         student.is_student = is_student
        #         student.save()
        #         # Save enrollments for the selected courses
        # courses = self.cleaned_data.get('courses')
        # if courses:
        #     for course in courses:
        #         Enrollment.objects.get_or_create(user=user, course=course)
        return user