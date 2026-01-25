import csv
import io
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.urls import reverse_lazy
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.core.exceptions import PermissionDenied

from .models import Project
from .forms import ProjectForm
from companies.models import Company
from core.permissions import can_manage_projects, can_access_projects_area


def get_user_company(user):
    """
    Retorna a empresa vinculada ao usuário (representante).
    """
    return Company.objects.filter(representante__email=user.email).first()


# =========================
# LISTAR PROJETOS
# =========================
@method_decorator(login_required, name="dispatch")
class ProjectListView(ListView):
    model = Project
    template_name = "projects/project_list.html"
    context_object_name = "projects"

    def dispatch(self, request, *args, **kwargs):
        if not can_access_projects_area(request.user):
            messages.error(request, "Você não tem permissão para acessar Projetos.")
            return redirect("home")
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        user = self.request.user

        # Gestores veem todos os projetos
        if can_manage_projects(user):
            return Project.objects.all()

        # Representantes veem apenas os da sua empresa
        company = get_user_company(user)
        if not company:
            messages.warning(
                self.request,
                "Você não possui empresa vinculada. Nenhum projeto disponível.",
            )
            return Project.objects.none()

        return Project.objects.filter(company=company)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["can_create_project"] = can_access_projects_area(self.request.user)
        return context


# =========================
# CRIAR PROJETO
# =========================
@method_decorator(login_required, name="dispatch")
class ProjectCreateView(CreateView):
    model = Project
    form_class = ProjectForm
    template_name = "projects/project_form.html"
    success_url = reverse_lazy("project_list")

    def dispatch(self, request, *args, **kwargs):
        if not can_access_projects_area(request.user):
            messages.error(request, "Você não tem permissão para criar projetos.")
            return redirect("home")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = self.request.user

        # Gestores escolhem a empresa
        if can_manage_projects(user):
            company = form.cleaned_data.get("company")
            if not company:
                messages.error(
                    self.request, "Selecione uma empresa válida para o projeto."
                )
                return self.form_invalid(form)

            form.instance.company = company
            return super().form_valid(form)

        # Representantes usam a empresa vinculada
        company = get_user_company(user)
        if not company:
            messages.error(
                self.request,
                "Você não tem uma empresa vinculada. Entre em contato com a diretoria.",
            )
            return redirect("project_list")

        form.instance.company = company
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request, "Erro ao criar o projeto. Verifique os campos informados."
        )
        return super().form_invalid(form)


@method_decorator(login_required, name="dispatch")
class ProjectDetailView(DetailView):
    model = Project
    template_name = "projects/project_detail.html"

    def get_object(self):
        project = get_object_or_404(Project, pk=self.kwargs["pk"])
        user = self.request.user

        if can_manage_projects(user):
            return project

        representante = getattr(project.company, "representante", None)
        if not representante or representante.email != user.email:
            raise PermissionDenied("Você não tem permissão para acessar este projeto.")

        return project


@method_decorator(login_required, name="dispatch")
class ProjectUpdateView(UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = "projects/project_form.html"
    success_url = reverse_lazy("project_list")

    def get_object(self):
        project = get_object_or_404(Project, pk=self.kwargs["pk"])
        user = self.request.user

        # Gestores podem editar tudo
        if can_manage_projects(user):
            return project

        representante = getattr(project.company, "representante", None)
        if not representante or representante.email != user.email:
            raise PermissionDenied("Você não tem permissão para editar este projeto.")

        return project

    def form_invalid(self, form):
        messages.error(
            self.request, "Erro ao atualizar o projeto. Verifique os dados informados."
        )
        return super().form_invalid(form)


@login_required
def project_export_csv(request):
    # Verifica permissão (apenas gestores)
    if not can_manage_projects(request.user):
        messages.error(request, "Você não tem permissão para exportar projetos.")
        return redirect("home")

    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="relatorio_projetos.csv"'
    response.write("\ufeff".encode("utf8"))

    writer = csv.writer(response, delimiter=";")
    writer.writerow(["ID", "Projeto", "Empresa", "Gênero", "Status", "Data Criação"])

    for project in (
        Project.objects.select_related("company").all().order_by("-created_at")
    ):
        writer.writerow(
            [
                project.id,
                project.name,
                project.company.nome_fantasia,
                project.get_genre_display(),
                project.get_status_display(),
                project.created_at.strftime("%d/%m/%Y"),
            ]
        )

    return response


@login_required
def project_export_pdf(request):
    if not can_manage_projects(request.user):
        messages.error(request, "Você não tem permissão para exportar projetos.")
        return redirect("home")

    projects = Project.objects.select_related("company").all().order_by("-created_at")
    context = {"projects": projects, "title": "Relatório de Projetos"}

    template_path = "projects/report_pdf.html"

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="relatorio_projetos.pdf"'

    template = get_template(template_path)
    html = template.render(context)

    pisa_status = pisa.CreatePDF(
        io.BytesIO(html.encode("UTF-8")),
        dest=response,
        encoding="UTF-8",
    )

    if pisa_status.err:
        return HttpResponse("Erro ao gerar PDF <pre>" + html + "</pre>")

    return response
