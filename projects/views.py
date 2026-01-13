from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Project
from companies.models import Company

@login_required
def project_list(request):
    user = request.user

    if user.is_staff:
        projects = Project.objects.all()
    else:
        projects = Project.objects.filter(company=user.company)

    return render(request, 'projects/list.html', {'projects': projects})


@login_required
def project_detail(request, pk):
    project = get_object_or_404(Project, pk=pk)

    if not request.user.is_staff and project.company != request.user.company:
        return redirect('project_list')

    return render(request, 'projects/detail.html', {'project': project})


@login_required
def project_create(request):
    if request.method == 'POST':
        Project.objects.create(
            name=request.POST['name'],
            description=request.POST['description'],
            status=request.POST['status'],
            company=request.user.company
        )
        return redirect('project_list')

    return render(request, 'projects/create.html')


@login_required
def project_update(request, pk):
    project = get_object_or_404(Project, pk=pk)

    if not request.user.is_staff and project.company != request.user.company:
        return redirect('project_list')

    if request.method == 'POST':
        project.name = request.POST['name']
        project.description = request.POST['description']
        project.status = request.POST['status']
        project.save()
        return redirect('project_detail', pk=pk)

    return render(request, 'projects/edit.html', {'project': project})
