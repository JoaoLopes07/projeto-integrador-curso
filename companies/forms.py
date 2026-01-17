from django import forms
from .models import Company, Representante

class RepresentanteForm(forms.ModelForm):
    class Meta:
        model = Representante
        fields = '__all__'


class CompanyForm(forms.ModelForm):
    
    cnpj = forms.CharField(max_length=20, required=True)
    cep = forms.CharField(max_length=20, required=True)
    telefone = forms.CharField(max_length=20, required=True)
    class Meta:
        model = Company
        fields = '__all__'
        
    def clean_cnpj(self):
        cnpj = self.cleaned_data.get("cnpj", "")
        cnpj = "".join(ch for ch in cnpj if ch.isdigit())
        if len(cnpj) != 14:
            raise forms.ValidationError("CNPJ deve conter 14 dígitos (apenas números).")
        return cnpj

    def clean_cep(self):
        cep = self.cleaned_data.get("cep", "")
        cep = "".join(ch for ch in cep if ch.isdigit())
        if len(cep) != 8:
            raise forms.ValidationError("CEP deve conter 8 dígitos (apenas números).")
        return cep

    def clean_telefone(self):
        tel = self.cleaned_data.get("telefone", "")
        tel = "".join(ch for ch in tel if ch.isdigit())
        if len(tel) not in (10, 11):
            raise forms.ValidationError("Telefone deve conter 10 ou 11 dígitos (apenas números).")
        return tel   
