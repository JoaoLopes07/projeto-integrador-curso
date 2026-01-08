from rest_framework import serializers
from .models import Company, Representante

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

class RepresentanteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Representante
        fields = [
            'id',
            'nome_completo',
            'nome_social',
            'cpf',
            'email',
            'telefone',
            'nick_discord',
            'cep',
            'endereco',
            'numero',
            'complemento',
            'bairro',
            'cidade',
            'estado',
        ]
        
