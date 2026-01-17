from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib import messages
from .models import Project
from .forms import ProjectForm
from companies.models import Company
from core.permissions import can_manage_projects, can_access_projects_area

def get_user_company(user):
    return Company.objects.filter(representante__email=user.email).first()

@method_decorator(login_required, name='dispatch')
class ProjectListView(ListView):
    model = Project
    template_name = 'projects/project_list.html'
    context_object_name = "projects"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context["can_create_project"] = can_access_projects_area(user)
        return context
    
    def dispatch(self, request, *args, **kwargs):
        user = request.user

        if not can_access_projects_area(user):
            messages.error(request, "Você não tem permissão para acessar Projetos.")
            return redirect("home")
        
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        user = self.request.user

        if can_manage_projects(user):
            return Project.objects.all()
        
        company = get_user_company(user)
        if not company:
            
            return Project.objects.none()

        return Project.objects.filter(company=company)


@method_decorator(login_required, name='dispatch')
class ProjectCreateView(CreateView):
    model = Project
    form_class = ProjectForm
    template_name = 'projects/project_form.html'
    success_url = reverse_lazy('project_list')
    
    def dispatch(self, request, *args, **kwargs):
        user = request.user
        
        if not can_access_projects_area(user):
            messages.error(request, "Você não tem permissão para criar projetos.")
            return redirect("home")
        
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = self.request.user

        if can_manage_projects(user):
            return super().form_valid(form)

        company = get_user_company(user)
        if company is None:
             messages.error(
                self.request,
                "Você não tem uma empresa vinculada. Entre em contato com a diretoria para vincular sua empresa antes de cadastrar projetos."
                )
             return redirect('project_list')

        form.instance.company = company

        return super().form_valid(form)



@method_decorator(login_required, name='dispatch')
class ProjectDetailView(DetailView):
    model = Project
    template_name = 'projects/project_detail.html'

    def dispatch(self, request, *args, **kwargs):
        user = request.user

        if can_manage_projects(user):
            return super().dispatch(request, *args, **kwargs) 
        
        project = self.get_object()
        representante = getattr(project.company, "representante", None)
        if representante is None or representante.email != user.email:
            messages.error(request, "Você não tem permissão para acessar este projeto.")
            return redirect("project_list")

        return super().dispatch(request, *args, **kwargs)


@method_decorator(login_required, name='dispatch')
class ProjectUpdateView(UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = 'projects/project_form.html'
    success_url = reverse_lazy('project_list')

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        
        if can_manage_projects(user):
            return super().dispatch(request, *args, **kwargs)

        project = self.get_object()
        representante = getattr(project.company, "representante", None)
        if representante is None or representante.email != user.email:
            messages.error(request, "Você não tem permissão para editar este projeto.")
            return redirect("project_list")

        return super().dispatch(request, *args, **kwargs)
