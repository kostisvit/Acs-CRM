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
            "start_date": forms.DateInput(
                attrs={"type": "date"}
            ),
            "end_date": forms.DateInput(
                attrs={"type": "date"}
            ),
            "description": forms.Textarea(
                attrs={"rows": 4}
            ),
            "info": forms.Textarea(
                attrs={"rows": 4}
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
            "file",
            "notes",
        )

        widgets = {
            "due_date": forms.DateInput(
                attrs={"type": "date"}
            ),
            "description": forms.Textarea(
                attrs={"rows": 3}
            ),
            "notes": forms.Textarea(
                attrs={"rows": 3}
            ),
        }
