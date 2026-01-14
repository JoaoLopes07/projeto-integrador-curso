from django import forms
from .models import Company, Representante

class RepresentanteForm(forms.ModelForm):
    class Meta:
        model = Representante
        fields = '__all__'


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = '__all__'
