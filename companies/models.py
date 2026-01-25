from django.db import models
from geopy.geocoders import Nominatim


class Representante(models.Model):
    nome_completo = models.CharField(max_length=255)
    nome_social = models.CharField(max_length=255, blank=True)
    cpf = models.CharField(max_length=11, unique=True)
    email = models.EmailField()
    telefone = models.CharField(max_length=11)
    nick_discord = models.CharField(max_length=255, blank=True, null=True)

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
        related_name="companies",
    )

    nome_fantasia = models.CharField(max_length=255)
    razao_social = models.CharField(max_length=255)
    cnpj = models.CharField(max_length=14, unique=True)
    email_contato = models.EmailField()
    telefone = models.CharField(max_length=11)
    site = models.URLField(blank=True, verbose_name="Site Oficial")

    # --- NOVOS CAMPOS (ITEM 4.5 - Sessão de Links) ---
    link_vagas = models.URLField(blank=True, verbose_name="Página de Vagas / Carreiras")
    link_linkedin = models.URLField(blank=True, verbose_name="LinkedIn")
    link_instagram = models.URLField(blank=True, verbose_name="Instagram")
    link_facebook = models.URLField(blank=True, verbose_name="Facebook")
    link_twitter = models.URLField(blank=True, verbose_name="X (Twitter)")
    link_portfolio = models.URLField(blank=True, verbose_name="Portfólio ou Parceiros")
    # -------------------------------------------------

    cep = models.CharField(max_length=8)
    endereco = models.CharField(max_length=255)
    numero = models.CharField(max_length=10)
    complemento = models.CharField(max_length=255, blank=True)
    bairro = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=2)

    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    AREA_CHOICES = [
        ("dev", "Desenvolvimento"),
        ("art", "Arte/Design"),
        ("audio", "Áudio/Música"),
        ("edu", "Educação"),
        ("pub", "Publisher"),
        ("outros", "Outros"),
    ]
    area_atuacao = models.CharField(
        max_length=50,
        choices=AREA_CHOICES,
        default="dev",
        verbose_name="Área de Atuação",
    )

    def save(self, *args, **kwargs):

        if not self.latitude or not self.longitude:
            try:
                geolocator = Nominatim(user_agent="acjogos_intranet_system_v2")

                cep_limpo = self.cep.replace("-", "").replace(".", "")

                busca_precisa = f"{self.endereco}, {self.numero}, {self.bairro}, {self.cidade} - {self.estado}, {cep_limpo}, Brazil"
                location = geolocator.geocode(busca_precisa)

                if not location:
                    print(
                        f"Busca precisa falhou para '{self.nome_fantasia}'. Tentando por CEP..."
                    )
                    busca_cep = f"{cep_limpo}, Brazil"
                    location = geolocator.geocode(busca_cep)

                if location:
                    self.latitude = location.latitude
                    self.longitude = location.longitude
                else:
                    print(
                        f"Atenção: Não foi possível localizar o endereço para '{self.nome_fantasia}'."
                    )

            except Exception as e:
                print(f"Erro ao conectar com serviço de mapas: {e}")

        super().save(*args, **kwargs)

    def __str__(self):
        return self.nome_fantasia
