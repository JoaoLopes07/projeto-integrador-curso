from django import forms
from django.forms import inlineformset_factory
from .models import Project, ProjectImage, ProjectLink


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ["company", "name", "description", "status"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4, "class": "form-control"}),
        }


ProjectImageFormSet = inlineformset_factory(
    Project,
    ProjectImage,
    fields=["image", "caption"],
    extra=1,
    can_delete=True,
)

ProjectLinkFormSet = inlineformset_factory(
    Project,
    ProjectLink,
    fields=["label", "url"],
    extra=1,
    can_delete=True,
    widgets={
        "label": forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Ex: Trailer YouTube, Steam, Site Oficial",
            }
        ),
        "url": forms.URLInput(
            attrs={"class": "form-control", "placeholder": "https://..."}
        ),
    },
)
