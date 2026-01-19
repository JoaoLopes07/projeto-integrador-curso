from django.shortcuts import render
from django.contrib.auth.decorators import (
    user_passes_test,
)
from companies.models import Company
from projects.models import Project
from django.db.models import Count, Q



def landing(request):
    return render(request, "public/landing.html")


def check_admin_access(user):
    return user.is_authenticated and (user.is_staff or user.is_superuser)



def map_view(request):
    empresas = Company.objects.filter(latitude__isnull=False, longitude__isnull=False)

    empresas_data = []
    for emp in empresas:
        empresas_data.append(
            {
                "nome": emp.nome_fantasia,
                "cidade": emp.cidade,
                "lat": emp.latitude,
                "lng": emp.longitude,
                "url": emp.site if emp.site else "#",
            }
        )

    context = {"empresas_json": empresas_data}

    return render(request, "public/map.html", context)


def diretorio(request):
    cidade = (request.GET.get("cidade") or "").strip()
    estado = (request.GET.get("estado") or "").strip()
    status = (request.GET.get("status") or "").strip()  

    companies = Company.objects.all()

    if cidade:
        companies = companies.filter(cidade__icontains=cidade)
    if estado:
        companies = companies.filter(estado__iexact=estado)

    if status:
        companies = companies.annotate(
            projects_count=Count("projects", filter=Q(projects__status=status))
        ).filter(projects_count__gt=0)
    else:
        companies = companies.annotate(projects_count=Count("projects"))


    
    if status:
        companies = companies.annotate(
            projects_count=Count("projects", filter=Q(projects__status=status))
        )
    else:
        companies = companies.annotate(projects_count=Count("projects"))

    
    estados_disponiveis = (
        Company.objects.values_list("estado", flat=True)
        .exclude(estado__isnull=True)
        .exclude(estado__exact="")
        .distinct()
        .order_by("estado")
    )

    cidades_disponiveis = []

    if estado:
        cidades_disponiveis = (
            Company.objects.filter(estado__iexact=estado)
            .values_list("cidade", flat=True)
            .exclude(cidade__isnull=True)
            .exclude(cidade__exact="")
            .distinct()
            .order_by("cidade")
        )


    status_choices = Project.STATUS_CHOICES

    context = {
        "companies": companies,
        "filters": {"cidade": cidade, "estado": estado, "status": status},
        "estados_disponiveis": estados_disponiveis,
        "cidades_disponiveis": cidades_disponiveis,
        "status_choices": status_choices,
    }
    return render(request, "public/diretorio.html", context)


def estatisticas(request):
    total_companies = Company.objects.count()
    total_projects = Project.objects.count()

    companies_por_estado = (
        Company.objects.values("estado")
        .annotate(total=Count("id"))
        .order_by("-total", "estado")
    )

    companies_por_cidade = (
        Company.objects.values("cidade")
        .annotate(total=Count("id"))
        .order_by("-total", "cidade")[:20]
    )

    projects_por_status = (
        Project.objects.values("status")
        .annotate(total=Count("id"))
        .order_by("-total", "status")
    )

    context = {
        "total_companies": total_companies,
        "total_projects": total_projects,
        "companies_por_estado": companies_por_estado,
        "companies_por_cidade": companies_por_cidade,
        "projects_por_status": projects_por_status,
        "status_choices": dict(Project.STATUS_CHOICES),
    }
    return render(request, "public/estatisticas.html", context)
