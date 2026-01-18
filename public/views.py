from django.shortcuts import render
from django.contrib.auth.decorators import (
    user_passes_test,
)
from companies.models import Company


def landing(request):
    return render(request, "public/landing.html")


def check_admin_access(user):
    return user.is_authenticated and (user.is_staff or user.is_superuser)


@user_passes_test(check_admin_access)
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
