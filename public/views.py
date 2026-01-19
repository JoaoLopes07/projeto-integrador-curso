from django.shortcuts import render
from companies.models import Company
from projects.models import Project
from django.db.models import Count, Q
import json


def landing(request):
    return render(request, "public/landing.html")


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

    locations = (
        Company.objects.exclude(estado="")
        .exclude(cidade="")
        .values("estado", "cidade")
        .distinct()
    )

    mapa_cidades = {}
    todos_estados = set()

    for loc in locations:
        uf = loc["estado"]
        cid = loc["cidade"]
        todos_estados.add(uf)

        if uf not in mapa_cidades:
            mapa_cidades[uf] = []
        if cid not in mapa_cidades[uf]:
            mapa_cidades[uf].append(cid)

    for uf in mapa_cidades:
        mapa_cidades[uf].sort()

    status_choices = Project.STATUS_CHOICES

    context = {
        "companies": companies,
        "filters": {"cidade": cidade, "estado": estado, "status": status},
        "estados_disponiveis": sorted(list(todos_estados)),
        "mapa_cidades_json": json.dumps(mapa_cidades),
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

    companies_por_cidade = list(
        Company.objects.values("cidade")
        .annotate(total=Count("id"))
        .order_by("-total", "cidade")[:20]
    )

    projects_por_status = list(
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
