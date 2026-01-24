from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import get_user_model
from core.permissions import (
    can_manage_companies,
    can_manage_projects,
    can_access_projects_area,
)

from companies.models import Company, Representante
from projects.models import Project
from surveys.models import SurveyResponse

User = get_user_model()


@login_required
def redirect_after_login(request):
    user = request.user
    if can_manage_companies(user):
        return redirect("dashboard_diretoria")
    if can_manage_projects(user):
        return redirect("project_list")
    if can_access_projects_area(user):
        return redirect("project_list")
    return redirect("home")


@login_required
@user_passes_test(can_manage_companies, login_url="/accounts/home/")
def dashboard_diretoria(request):

    context = {
        "total_companies": Company.objects.count(),
        "total_representantes": Representante.objects.count(),
        "total_projects": Project.objects.count(),
        # Conta quantas respostas de pesquisa existem no total
        "total_surveys": SurveyResponse.objects.count(),
    }
    return render(request, "dashboard/diretoria/home.html", context)


def home(request):

    context = {
        "total_companies": Company.objects.count(),
        "total_projects": Project.objects.count(),
        "total_users": User.objects.count(),
    }
    return render(request, "public/landing.html", context)
