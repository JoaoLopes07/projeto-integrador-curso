from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Company, Representante
from .forms import (
    CompanyForm,
    RepresentanteForm,
    RepresentantePublicForm,
    CompanyPublicForm,
)
from core.permissions import can_manage_companies

from django.views import View
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import transaction


admin_required = [
    login_required,
    user_passes_test(can_manage_companies, login_url="/accounts/home/"),
]


@method_decorator(admin_required, name="dispatch")
class CompanyListView(ListView):
    model = Company
    template_name = "company/company_list.html"


@method_decorator(admin_required, name="dispatch")
class CompanyCreateView(CreateView):
    model = Company
    form_class = CompanyForm
    template_name = "company/company_form.html"
    success_url = reverse_lazy("company-list")


@method_decorator(admin_required, name="dispatch")
class CompanyUpdateView(UpdateView):
    model = Company
    form_class = CompanyForm
    template_name = "company/company_form.html"
    success_url = reverse_lazy("company-list")


@method_decorator(admin_required, name="dispatch")
class CompanyDeleteView(DeleteView):
    model = Company
    success_url = reverse_lazy("company-list")


@method_decorator(admin_required, name="dispatch")
class RepresentanteListView(ListView):
    model = Representante
    template_name = "representante/representante_list.html"


@method_decorator(admin_required, name="dispatch")
class RepresentanteCreateView(CreateView):
    model = Representante
    form_class = RepresentanteForm
    template_name = "representante/representante_form.html"
    success_url = reverse_lazy("representante-list")


@method_decorator(admin_required, name="dispatch")
class RepresentanteUpdateView(UpdateView):
    model = Representante
    form_class = RepresentanteForm
    template_name = "representante/representante_form.html"
    success_url = reverse_lazy("representante-list")


@method_decorator(admin_required, name="dispatch")
class RepresentanteDeleteView(DeleteView):
    model = Representante
    success_url = reverse_lazy("representante-list")


class CompanyPublicRegisterView(View):
    template_name = "company/company_public_register.html"

    def get(self, request):
        return render(
            request,
            self.template_name,
            {
                "rep_form": RepresentantePublicForm(),
                "company_form": CompanyPublicForm(),
            },
        )

    def post(self, request):
        rep_form = RepresentantePublicForm(request.POST)
        company_form = CompanyPublicForm(request.POST)

        if rep_form.is_valid() and company_form.is_valid():
            with transaction.atomic():
                representante = rep_form.save()
                company = company_form.save(commit=False)
                company.representante = representante
                company.save()

            messages.success(
                request,
                "Empresa cadastrada com sucesso! Em breve entraremos em contato.",
            )
            return redirect("login")  # ou uma página “sucesso”

        messages.error(request, "Corrija os campos destacados e tente novamente.")
        return render(
            request,
            self.template_name,
            {
                "rep_form": rep_form,
                "company_form": company_form,
            },
        )


method_decorator(login_required, name="dispatch")


class CompanyMyUpdateView(UpdateView):
    model = Company
    form_class = CompanyForm
    template_name = "company/company_form.html"
    success_url = reverse_lazy("home")

    def get_object(self, queryset=None):

        return get_object_or_404(Company, representante__email=self.request.user.email)

    def form_valid(self, form):
        messages.success(self.request, "Dados da sua empresa atualizados com sucesso!")
        return super().form_valid(form)
