from django.contrib import admin
from .models import Company, Representante


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):

    list_display = ("nome_fantasia", "cidade", "latitude", "longitude")

    search_fields = ("nome_fantasia",)

    fields = (
        "nome_fantasia",
        "razao_social",
        "cnpj",
        "email_contato",
        "telefone",
        "site",
        "cep",
        "endereco",
        "numero",
        "complemento",
        "bairro",
        "cidade",
        "estado",
        "latitude",
        "longitude",
        "representante",
    )


admin.site.register(Representante)
