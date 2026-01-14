from django.db import models

class Representante(models.Model):
    nome_completo = models.CharField(max_length=255)
    nome_social = models.CharField(max_length=255, blank=True)
    cpf = models.CharField(max_length=11, unique=True)
    email = models.EmailField()
    telefone = models.CharField(max_length=11)
    nick_discord = models.CharField(max_length=255)

    cep = models.CharField(max_length=8)
    endereco = models.CharField(max_length=255)
    numero = models.CharField(max_length=10)
    complemento = models.CharField(max_length=255, blank=True)
    bairro = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=2)

    def __str__(self):
        return self.nome_completo


class Company(models.Model):
    representante = models.ForeignKey(
        Representante,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='companies'
    )

    nome_fantasia = models.CharField(max_length=255)
    razao_social = models.CharField(max_length=255)
    cnpj = models.CharField(max_length=14, unique=True)
    email_contato = models.EmailField()
    telefone = models.CharField(max_length=11)
    site = models.URLField(blank=True)

    cep = models.CharField(max_length=8)
    endereco = models.CharField(max_length=255)
    numero = models.CharField(max_length=10)
    complemento = models.CharField(max_length=255, blank=True)
    bairro = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=2)

    def __str__(self):
        return self.nome_fantasia
