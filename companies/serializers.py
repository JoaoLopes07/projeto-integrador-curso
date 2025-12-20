from rest_framework import serializers
from .models import Company

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = [
            'nome_fantasia', 
            'razao_social', 
            'cnpj', 
            'email_contato', 
            'telefone', 
            'site', 
            'cep', 
            'endereco', 
            'numero', 
            'complemento', 
            'bairro', 
            'cidade', 
            'estado',
            'representante',
        ]
