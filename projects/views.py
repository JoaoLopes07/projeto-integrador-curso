from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
    DetailView,
)
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db import transaction
from django.contrib import messages

from .models import Project
from .forms import ProjectForm, ProjectImageFormSet, ProjectLinkFormSet


@method_decorator(login_required, name="dispatch")
class ProjectListView(ListView):
    model = Project
    template_name = "projects/project_list.html"
    context_object_name = "projects"

    def get_queryset(self):
        user = self.request.user

        if user.role == "diretoria":
            return Project.objects.all().order_by("-created_at")

        return Project.objects.all().order_by("-created_at")


@method_decorator(login_required, name="dispatch")
class ProjectDetailView(DetailView):
    model = Project
    template_name = "projects/project_detail.html"
    context_object_name = "project"


@method_decorator(login_required, name="dispatch")
class ProjectCreateView(CreateView):
    model = Project
    form_class = ProjectForm
    template_name = "projects/project_form.html"
    success_url = reverse_lazy("project_list")

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:

            data["images"] = ProjectImageFormSet(self.request.POST, self.request.FILES)
            data["links"] = ProjectLinkFormSet(self.request.POST)
        else:

            data["images"] = ProjectImageFormSet()
            data["links"] = ProjectLinkFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        images = context["images"]
        links = context["links"]

        with transaction.atomic():
            self.object = form.save()

            if images.is_valid():
                images.instance = self.object
                images.save()

            if links.is_valid():
                links.instance = self.object
                links.save()

        messages.success(self.request, "Projeto criado com sucesso!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request, "Erro ao criar projeto. Verifique os campos abaixo."
        )
        return super().form_invalid(form)


@method_decorator(login_required, name="dispatch")
class ProjectUpdateView(UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = "projects/project_form.html"
    success_url = reverse_lazy("project_list")

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            # Popula com dados do POST e vincula à instância atual do projeto
            data["images"] = ProjectImageFormSet(
                self.request.POST, self.request.FILES, instance=self.object
            )
            data["links"] = ProjectLinkFormSet(self.request.POST, instance=self.object)
        else:
            # Popula com dados do banco (para edição)
            data["images"] = ProjectImageFormSet(instance=self.object)
            data["links"] = ProjectLinkFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        images = context["images"]
        links = context["links"]

        with transaction.atomic():
            self.object = form.save()

            if images.is_valid():
                images.save()

            if links.is_valid():
                links.save()

        messages.success(self.request, "Projeto atualizado com sucesso!")
        return super().form_valid(form)


@method_decorator(login_required, name="dispatch")
class ProjectDeleteView(DeleteView):
    model = Project
    template_name = "projects/project_confirm_delete.html"
    success_url = reverse_lazy("project_list")

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Projeto excluído com sucesso.")
        return super().delete(request, *args, **kwargs)
