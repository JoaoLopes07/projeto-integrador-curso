from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required, user_passes_test
from core.permissions import (
    can_manage_companies,
    can_manage_projects,
    can_access_projects_area
)

@login_required
def redirect_after_login(request):
    user = request.user

    if can_manage_companies(user):
        return redirect('dashboard_diretoria')

    if can_manage_projects(user):
        return redirect('project_list')

    if can_access_projects_area(user):
        return redirect('project_list')

    return redirect('home')

@login_required
@user_passes_test(can_manage_companies, login_url="/accounts/home/")
def dashboard_diretoria(request):
    return render(request, "dashboard/diretoria/home.html")

