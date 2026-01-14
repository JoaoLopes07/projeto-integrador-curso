from django import forms
from .models import SurveyResponse


class SurveyResponseForm(forms.ModelForm):
    class Meta:
        model = SurveyResponse
        fields = [
            "company_size",
            "annual_revenue",
            "main_difficulty",
        ]

        widgets = {
            "company_size": forms.TextInput(attrs={
                "class": "form-control"
            }),
            "annual_revenue": forms.TextInput(attrs={
                "class": "form-control"
            }),
            "main_difficulty": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 4
            }),
        }
        
