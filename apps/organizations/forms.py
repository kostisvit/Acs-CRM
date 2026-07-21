# forms.py
from django import forms
from .models import Organization


INPUT_CLASS = (
    "block w-full rounded-lg border border-gray-300 bg-white px-3 py-2 "
    "text-sm shadow-sm placeholder:text-gray-400 "
    "focus:border-teal-300 focus:ring-2 focus:ring-teal-400"
)

TEXTAREA_CLASS = (
    "block w-full rounded-lg border border-gray-300 bg-white px-3 py-2 "
    "text-sm shadow-sm placeholder:text-gray-400 "
    "focus:border-teal-300 focus:ring-2 focus:ring-teal-400"
)




class CSVUploadForm(forms.Form):
    csv_file = forms.FileField()
    

class OrganizationForm(forms.ModelForm):
    class Meta:
        model = Organization
        fields = "__all__"

        widgets = {
            "org_name": forms.TextInput(attrs={"class": INPUT_CLASS}),
            "org_address": forms.TextInput(attrs={"class": INPUT_CLASS}),
            "org_city": forms.TextInput(attrs={"class": INPUT_CLASS}),
            "org_phone": forms.TextInput(attrs={"class": INPUT_CLASS}),
            "org_remote": forms.TextInput(attrs={"class": INPUT_CLASS}),
            "org_email": forms.EmailInput(attrs={"class": INPUT_CLASS}),
            "org_site": forms.URLInput(attrs={"class": INPUT_CLASS}),
            "org_info": forms.Textarea(
                attrs={
                    "class": TEXTAREA_CLASS,
                    "rows": 5,
                }
            ),
            "is_visible": forms.CheckboxInput(
                attrs={
                    "class": "h-5 w-5 rounded border-gray-300 text-indigo-600 focus:ring-indigo-500"
                }
            ),
        }