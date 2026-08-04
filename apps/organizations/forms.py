# forms.py
from django import forms

from .models import Organization, Employee, Task

INPUT_CLASS = (
    "block w-full rounded-lg border border-gray-300 bg-white px-3 py-2 "
    "text-sm shadow-sm placeholder:text-gray-400 "
    "focus:border-teal-300 focus:ring-2 focus:ring-teal-400 focus:outline-none"
)

TEXTAREA_CLASS = (
    "block w-full rounded-lg border border-gray-300 bg-white px-3 py-2 "
    "text-sm shadow-sm placeholder:text-gray-400 "
    "focus:border-teal-300 focus:ring-2 focus:ring-teal-400 focus:outline-none"
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
            "is_active": forms.CheckboxInput(
                attrs={
                    "class": "h-5 w-5 rounded border-gray-300 text-indigo-600 focus:ring-indigo-500"
                }
            ),
        }


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = "__all__"

        widgets = {
            "organization": forms.Select(
                attrs={"class": INPUT_CLASS}
            ),
            "firstname": forms.TextInput(
                attrs={"class": INPUT_CLASS}
            ),
            "lastname": forms.TextInput(
                attrs={"class": INPUT_CLASS}
            ),
            "phone": forms.TextInput(
                attrs={"class": INPUT_CLASS}
            ),
            "mobile": forms.TextInput(
                attrs={"class": INPUT_CLASS}
            ),
            "email": forms.EmailInput(
                attrs={"class": INPUT_CLASS}
            ),
            "secondary_email": forms.EmailInput(
                attrs={"class": INPUT_CLASS}
            ),
            "org_department": forms.Select(
                attrs={"class": INPUT_CLASS}
            ),
            "info": forms.Textarea(
                attrs={
                    "class": TEXTAREA_CLASS,
                    "rows": 5,
                }
            ),
            "is_active": forms.CheckboxInput(
                attrs={
                    "class": "h-5 w-5 rounded border-gray-300 text-indigo-600 focus:ring-indigo-500"
                }
            ),
        }


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = "__all__"

        widgets = {
            "organization": forms.Select(
                attrs={"class": INPUT_CLASS,
                       "id": "id_organization", },

            ),
            "importdate": forms.DateInput(
                attrs={
                    "class": INPUT_CLASS + " flatpickr",
                    "autocomplete": "off",
                },
            ),
            "org_app": forms.Select(
                attrs={"class": INPUT_CLASS}
            ),
            "job_type_acs": forms.Select(
                attrs={"class": INPUT_CLASS}
            ),
            "task_note": forms.Textarea(
                attrs={"class": TEXTAREA_CLASS, "rows": 5}
            ),
            "acs_employee": forms.Select(
                attrs={"class": INPUT_CLASS}
            ),
            "org_employee": forms.Select(
                attrs={"class": INPUT_CLASS,
                       "id": "id_org_employee", }
            ),
            "task_time": forms.TextInput(
                attrs={"class": INPUT_CLASS}
            ),
            "task_info": forms.Textarea(
                attrs={
                    "class": TEXTAREA_CLASS,
                    "rows": 5,
                }
            ),
        }

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields["importdate"].initial = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["importdate"].initial = None
        self.fields["org_employee"].queryset = Employee.objects.none()

        if self.data.get("organization"):
            self.fields["org_employee"].queryset = Employee.objects.filter(
                organization_id=self.data.get("organization")
            )

        elif self.instance.pk:
            try:
                self.fields["org_employee"].queryset = Employee.objects.filter(
                    organization=self.instance.organization
                )
            except Task.organization.RelatedObjectDoesNotExist:
                pass
