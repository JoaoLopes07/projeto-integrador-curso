import random
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from companies.models import Company, Representante
from projects.models import Project, ProjectLink, ProjectImage
from surveys.models import SurveyYear

User = get_user_model()


class Command(BaseCommand):
    help = "Popula o banco com dados realistas do ecossistema carioca."

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.WARNING("--- INICIANDO LIMPEZA DO BANCO ---"))

        ProjectLink.objects.all().delete()
        ProjectImage.objects.all().delete()
        Project.objects.all().delete()
        Company.objects.all().delete()
        Representante.objects.all().delete()

        User.objects.filter(role__in=["associado", "afiliado"]).delete()
        if User.objects.filter(username="diretor").exists():
            User.objects.get(username="diretor").delete()

        self.stdout.write("--- CRIANDO NOVOS DADOS ---")

        diretor = User.objects.create_user(
            username="diretor",
            email="diretor@acjogos.rj.gov.br",
            password="123",
            role="diretoria",
            first_name="Admin",
            last_name="Diretor",
            is_staff=True,
            is_superuser=True,
        )
        self.stdout.write(f"Diretoria criada: {diretor.email}")

        estudios = [
            {
                "nome": "Carioca Games Studio",
                "cnpj": "12.345.678/0001-01",
                "bairro": "Botafogo",
                "lat": -22.9519,
                "lon": -43.1841,
                "site": "https://cariocagames.com.br",
                "desc": "Especialistas em jogos mobile casuais.",
                "proj": "Beach Tennis Simulator 2026",
                "proj_desc": "O simulador definitivo do esporte.",
            },
            {
                "nome": "Pão de Açúcar Digital",
                "cnpj": "98.765.432/0001-02",
                "bairro": "Urca",
                "lat": -22.9556,
                "lon": -43.1662,
                "site": "https://pao-acucar-digital.com",
                "desc": "Jogos educativos e VR.",
                "proj": "Rio VR Experience",
                "proj_desc": "Uma viagem virtual pelo Rio Antigo.",
            },
            {
                "nome": "Barra Devs Interactive",
                "cnpj": "45.123.789/0001-03",
                "bairro": "Barra da Tijuca",
                "lat": -23.0007,
                "lon": -43.3557,
                "site": "https://barradevs.com",
                "desc": "Focados em Triple-A.",
                "proj": "Cyber Copacabana",
                "proj_desc": "RPG de ação cyberpunk.",
            },
            {
                "nome": "Lapa Indie Collective",
                "cnpj": "33.444.555/0001-04",
                "bairro": "Lapa",
                "lat": -22.9135,
                "lon": -43.1824,
                "site": "https://lapaindie.art",
                "desc": "Coletivo de arte e jogos.",
                "proj": "Bohemian Nights",
                "proj_desc": "Visual novel noir.",
            },
            {
                "nome": "Tijuca Tech Solutions",
                "cnpj": "11.222.333/0001-05",
                "bairro": "Tijuca",
                "lat": -22.9239,
                "lon": -43.2355,
                "site": "https://tijucatech.com.br",
                "desc": "Outsourcing de arte 3D.",
                "proj": "Server Tycoon",
                "proj_desc": "Gerencie datacenters.",
            },
        ]

        for i, dados in enumerate(estudios):
            username = f"estudio{i+1}"
            email = f"contato@estudio{i+1}.com"

            user = User.objects.create_user(
                username=username,
                email=email,
                password="123",
                role="associado",
                first_name="Gestor",
                last_name=dados["bairro"],
            )

            rep = Representante.objects.create(
                nome_completo=f'Fundador da {dados["nome"]}',
                cpf=f"1234567890{i}",  # CPF único para evitar o erro
                email=user.email,
                telefone="21999999999",
                cep="22222000",
                endereco=f'Rua do {dados["bairro"]}',
                numero=str(100 + i),
                bairro=dados["bairro"],
                cidade="Rio de Janeiro",
                estado="RJ",
            )

            empresa = Company.objects.create(
                representante=rep,
                cnpj=dados["cnpj"],
                nome_fantasia=dados["nome"],
                razao_social=f'{dados["nome"]} Ltda',
                email_contato=user.email,
                telefone="2122223333",
                site=dados["site"],
                cep="20000000",
                endereco=f'Avenida {dados["bairro"]}',
                numero=str(200 + i),
                bairro=dados["bairro"],
                cidade="Rio de Janeiro",
                estado="RJ",
                latitude=dados["lat"],
                longitude=dados["lon"],
                link_linkedin="https://linkedin.com",
                link_instagram="https://instagram.com",
            )

            proj = Project.objects.create(
                name=dados["proj"],
                company=empresa,
                description=dados["proj_desc"],
                status="active" if i % 2 == 0 else "pending",
            )

            ProjectLink.objects.create(
                project=proj, label="Trailer", url="https://youtube.com"
            )

            self.stdout.write(f'Criada empresa: {dados["nome"]}')

        SurveyYear.objects.get_or_create(year=2025, defaults={"is_active": True})

        self.stdout.write(
            self.style.SUCCESS("--- POVOAMENTO CONCLUÍDO COM SUCESSO! ---")
        )
