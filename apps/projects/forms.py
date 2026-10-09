from django import forms

from .models import Project, ProjectDocument


class ProjectForm(forms.ModelForm):

    class Meta:
        model = Project

        fields = (
            "organization",
            "title",
            "description",
            "start_date",
            "end_date",
            "responsible",
            "is_active",
            "info",
        )

        widgets = {
            "organization": forms.Select(
                attrs={
                    "class": (
                        "block w-full rounded-lg border border-gray-300 "
                        "bg-white px-3 py-2.5 text-sm text-gray-900 "
                        "shadow-sm outline-none "
                        "focus:border-indigo-500 "
                        "focus:ring-2 focus:ring-indigo-500/20 "
                        "cursor-pointer"
                    )
                }
            ),

            "start_date": forms.DateInput(
                format="%Y-%m-%d",
                attrs={
                    "type": "date",
                    "class": (
                        "w-full rounded-lg border border-gray-300 "
                        "bg-gray-50 px-4 py-2.5 text-sm text-gray-900 "
                        "focus:border-blue-500 focus:ring-blue-500"
                    ),
                },
            ),

            "end_date": forms.DateInput(
                format="%Y-%m-%d",
                attrs={
                    "type": "date",
                    "class": (
                        "w-full rounded-lg border border-gray-300 "
                        "bg-gray-50 px-4 py-2.5 text-sm text-gray-900 "
                        "focus:border-blue-500 focus:ring-blue-500"
                    ),
                },
            ),

            "description": forms.Textarea(
                attrs={
                    "rows": 4,
                    "class": (
                        "block w-full rounded-lg border border-gray-300 "
                        "bg-white px-3 py-2.5 text-sm text-gray-900 "
                        "focus:border-indigo-500 "
                        "focus:ring-2 focus:ring-indigo-500/20"
                    ),
                }
            ),
            "responsible": forms.Select(
                attrs={
                    "class": (
                        "block w-full rounded-lg border border-gray-300 "
                        "bg-white px-3 py-2.5 text-sm text-gray-900 "
                        "shadow-sm outline-none "
                        "focus:border-indigo-500 "
                        "focus:ring-2 focus:ring-indigo-500/20 "
                        "cursor-pointer"
                    )
                }
            ),

            "info": forms.Textarea(
                attrs={
                    "rows": 4,
                    "class": (
                        "block w-full rounded-lg border border-gray-300 "
                        "bg-white px-3 py-2.5 text-sm text-gray-900 "
                        "focus:border-indigo-500 "
                        "focus:ring-2 focus:ring-indigo-500/20"
                    ),
                }
            ),
        }


class ProjectDocumentForm(forms.ModelForm):

    class Meta:
        model = ProjectDocument

        fields = (
            "title",
            "description",
            "due_date",
            "responsible",
            "notes",
        )

        widgets = {

            "title": forms.TextInput(
                attrs={
                    "class": (
                        "block w-full rounded-lg border border-gray-300 "
                        "bg-white px-3 py-2.5 text-sm text-gray-900 "
                        "shadow-sm outline-none "
                        "placeholder:text-gray-400 "
                        "focus:border-indigo-500 "
                        "focus:ring-2 focus:ring-indigo-500/20"
                    ),
                    "placeholder": "π.χ. Τεχνική Έκθεση",
                }
            ),

            "due_date": forms.DateInput(
                attrs={
                    "type": "date",
                    "class": (
                        "block w-full rounded-lg border border-gray-300 "
                        "bg-white px-3 py-2.5 text-sm text-gray-900 "
                        "shadow-sm outline-none "
                        "focus:border-indigo-500 "
                        "focus:ring-2 focus:ring-indigo-500/20"
                    ),
                }
            ),

            "responsible": forms.Select(
                attrs={
                    "class": (
                        "block w-full rounded-lg border border-gray-300 "
                        "bg-white px-3 py-2.5 text-sm text-gray-900 "
                        "shadow-sm outline-none "
                        "focus:border-indigo-500 "
                        "focus:ring-2 focus:ring-indigo-500/20 "
                        "cursor-pointer"
                    )
                }
            ),

            "description": forms.Textarea(
                attrs={
                    "rows": 3,
                    "class": (
                        "block w-full rounded-lg border border-gray-300 "
                        "bg-white px-3 py-2.5 text-sm text-gray-900 "
                        "shadow-sm outline-none "
                        "placeholder:text-gray-400 "
                        "focus:border-indigo-500 "
                        "focus:ring-2 focus:ring-indigo-500/20 "
                        "resize-y"
                    ),
                    "placeholder": "Περιγραφή του εντύπου...",
                }
            ),

            "notes": forms.Textarea(
                attrs={
                    "rows": 3,
                    "class": (
                        "block w-full rounded-lg border border-gray-300 "
                        "bg-white px-3 py-2.5 text-sm text-gray-900 "
                        "shadow-sm outline-none "
                        "placeholder:text-gray-400 "
                        "focus:border-indigo-500 "
                        "focus:ring-2 focus:ring-indigo-500/20 "
                        "resize-y"
                    ),
                    "placeholder": "Πρόσθετες σημειώσεις...",
                }
            ),
        }



class ProjectDocumentSubmitForm(forms.ModelForm):

    class Meta:
        model = ProjectDocument
        fields = (
            "file",
        )

        widgets = {
            "file": forms.ClearableFileInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["file"].required = True
