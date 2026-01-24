from django import forms
from .models import Company, Representante
from django.db import transaction


class RepresentanteForm(forms.ModelForm):
    cpf = forms.CharField(max_length=20, required=True)
    cep = forms.CharField(max_length=20, required=True)
    telefone = forms.CharField(max_length=20, required=True)

    class Meta:
        model = Representante
        fields = "__all__"

    def clean_cpf(self):
        cpf = self.cleaned_data.get("cpf", "")
        cpf = "".join(ch for ch in cpf if ch.isdigit())

        if len(cpf) != 11:
            raise forms.ValidationError("CPF deve conter 11 dígitos (apenas números).")
        return cpf

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
            raise forms.ValidationError(
                "Telefone deve conter 10 ou 11 dígitos (apenas números)."
            )
        return tel

    def clean_estado(self):
        estado = (self.cleaned_data.get("estado") or "").strip().upper()
        if len(estado) != 2:
            raise forms.ValidationError("Estado deve conter 2 letras (UF). Ex: RJ, SP.")
        return estado


class CompanyForm(forms.ModelForm):
    cnpj = forms.CharField(max_length=20, required=True)
    cep = forms.CharField(max_length=20, required=True)
    telefone = forms.CharField(max_length=20, required=True)

    class Meta:
        model = Company
        fields = "__all__"

        widgets = {
            "latitude": forms.TextInput(
                attrs={
                    "placeholder": "Ex: -22.9035 (Gerado automaticamente)",
                    "class": "form-control",
                }
            ),
            "longitude": forms.TextInput(
                attrs={
                    "placeholder": "Ex: -43.1234 (Gerado automaticamente)",
                    "class": "form-control",
                }
            ),
            # --- Widgets para os novos Links ---
            "link_vagas": forms.URLInput(
                attrs={"class": "form-control", "placeholder": "https://..."}
            ),
            "link_linkedin": forms.URLInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "https://linkedin.com/...",
                }
            ),
            "link_instagram": forms.URLInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "https://instagram.com/...",
                }
            ),
            "link_facebook": forms.URLInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "https://facebook.com/...",
                }
            ),
            "link_twitter": forms.URLInput(
                attrs={"class": "form-control", "placeholder": "https://x.com/..."}
            ),
            "link_portfolio": forms.URLInput(
                attrs={"class": "form-control", "placeholder": "https://..."}
            ),
        }

        help_texts = {
            "latitude": "Deixe em branco para que o sistema busque automaticamente pelo endereço.",
            "longitude": "Caso o mapa mostre o local errado, insira as coordenadas manuais aqui.",
            "cep": "O CEP é essencial para garantir que o pino do mapa caia no local exato.",
            "bairro": "Informe o bairro corretamente para ajudar na precisão do mapa.",
        }

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
            raise forms.ValidationError(
                "Telefone deve conter 10 ou 11 dígitos (apenas números)."
            )
        return tel


class RepresentantePublicForm(forms.ModelForm):

    cpf = forms.CharField(max_length=20, required=True)
    cep = forms.CharField(max_length=20, required=True)
    telefone = forms.CharField(max_length=20, required=True)

    class Meta:

        model = Representante
        fields = [
            "nome_completo",
            "nome_social",
            "cpf",
            "email",
            "telefone",
            "nick_discord",
            "cep",
            "endereco",
            "numero",
            "complemento",
            "bairro",
            "cidade",
            "estado",
        ]

    def clean_cpf(self):
        cpf = self.cleaned_data.get("cpf", "")
        cpf = "".join(ch for ch in cpf if ch.isdigit())

        if len(cpf) != 11:
            raise forms.ValidationError("CPF deve conter 11 dígitos (apenas números).")
        return cpf

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
            raise forms.ValidationError(
                "Telefone deve conter 10 ou 11 dígitos (apenas números)."
            )
        return tel

    def clean_estado(self):
        estado = (self.cleaned_data.get("estado") or "").strip().upper()
        if len(estado) != 2:
            raise forms.ValidationError("Estado deve conter 2 letras (UF). Ex: RJ, SP.")
        return estado


class CompanyPublicForm(CompanyForm):

    cnpj = forms.CharField(max_length=20, required=True)
    cep = forms.CharField(max_length=20, required=True)
    telefone = forms.CharField(max_length=20, required=True)

    class Meta(CompanyForm.Meta):

        model = Company
        fields = [
            "nome_fantasia",
            "razao_social",
            "cnpj",
            "email_contato",
            "telefone",
            "site",
            # --- Novos campos adicionados aqui ---
            "link_vagas",
            "link_linkedin",
            "link_instagram",
            "link_facebook",
            "link_twitter",
            "link_portfolio",
            # -------------------------------------
            "cep",
            "endereco",
            "numero",
            "complemento",
            "bairro",
            "cidade",
            "estado",
            # latitude/longitude podem ficar de fora, pois são auto no save()
        ]

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
            raise forms.ValidationError(
                "Telefone deve conter 10 ou 11 dígitos (apenas números)."
            )
        return tel
