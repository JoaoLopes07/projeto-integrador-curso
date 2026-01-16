from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib import messages
from .models import Project
from .forms import ProjectForm
from companies.models import Company


def is_admin(user):
    return user.is_superuser or user.is_staff


@method_decorator(login_required, name='dispatch')
class ProjectListView(ListView):
    model = Project
    template_name = 'projects/project_list.html'
    context_object_name = "projects"

    def get_queryset(self):
        user = self.request.user

        if is_admin(user):
            return Project.objects.all()

        return Project.objects.filter(
            company__representante__email=user.email
        )


@method_decorator(login_required, name='dispatch')
class ProjectCreateView(CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'projects/project_form.html'
    success_url = reverse_lazy('project_list')

    def form_valid(self, form):
        user = self.request.user

        if not is_admin(user):
            company = Company.objects.filter(
                representante__email=user.email
            ).first()

            if company is None:
                messages.error(
                    self.request,
                    "Você não tem uma empresa vinculada. Solicite à diretoria/admin para vincular sua empresa antes de cadastrar projetos."
                )
                return redirect('project_list')

            form.instance.company = company

        return super().form_valid(form)



@method_decorator(login_required, name='dispatch')
class ProjectDetailView(DetailView):
    model = Project
    template_name = 'projects/project_detail.html'

    def dispatch(self, request, *args, **kwargs):
        project = self.get_object()
        user = request.user

        if not is_admin(user):
            representante = project.company.representante
            if representante is None or representante.email != user.email:
                messages.error(request, "Você não tem permissão para acessar este projeto.")
                return redirect('project_list')

        return super().dispatch(request, *args, **kwargs)


@method_decorator(login_required, name='dispatch')
class ProjectUpdateView(UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'projects/project_form.html'
    success_url = reverse_lazy('project_list')

    def dispatch(self, request, *args, **kwargs):
        project = self.get_object()
        user = request.user

        if not is_admin(user):
            representante = project.company.representante
            if representante is None or representante.email != user.email:
                messages.error(request, "Você não tem permissão para editar este projeto.")
                return redirect('project_list')

        return super().dispatch(request, *args, **kwargs)
