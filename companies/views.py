import csv
import io
import secrets
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import PasswordResetForm
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template.loader import get_template
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from xhtml2pdf import pisa

from core.permissions import can_manage_companies, can_view_company_data
from .forms import CompanyForm, CompanyPublicForm, RepresentanteForm, RepresentantePublicForm
from .models import Company, Representante


admin_required = [
    login_required,
    user_passes_test(can_view_company_data, login_url="/accounts/home/"),
]


@method_decorator(admin_required, name="dispatch")
class CompanyListView(ListView):
    model = Company
    template_name = "company/company_list.html"

    def get_queryset(self):
        user = self.request.user

        if can_manage_companies(user):  # diretoria pode ver todas
            return Company.objects.all()

        # associado: vê só as suas empresas
        return Company.objects.filter(representante__user=user)


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

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        user = self.request.user

        if can_manage_companies(user):  # diretoria pode editar todos
            return obj

        if obj.representante and obj.representante.user_id == user.id:
            return obj

        raise PermissionDenied("Você não tem permissão para editar esta empresa.")


@method_decorator(admin_required, name="dispatch")
class CompanyDeleteView(DeleteView):
    model = Company
    success_url = reverse_lazy("company-list")

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        user = self.request.user

        if can_manage_companies(user):
            return obj

        if obj.representante and obj.representante.user_id == user.id:
            return obj

        raise PermissionDenied("Você não tem permissão para excluir esta empresa.")


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

    def form_valid(self, form):
        User = get_user_model()

        with transaction.atomic():
            representante = form.save(commit=False)

            user = User.objects.filter(email__iexact=representante.email).first()

            if user:
                if hasattr(user, "role"):
                    user.role = "associado"
                    user.save(update_fields=["role"])
            else:
                email = representante.email.strip().lower()

                user = User.objects.create_user(username=email, email=email)

                temp_password = secrets.token_urlsafe(16)
                user.set_password(temp_password)
                user.save(update_fields=["password"])

                if hasattr(user, "role"):
                    user.role = "associado"
                    user.save(update_fields=["role"])

                reset_form = PasswordResetForm({"email": user.email})
                if reset_form.is_valid():
                    reset_form.save(
                        request=self.request,
                        use_https=self.request.is_secure(),
                        email_template_name="registration/password_reset_email.html",
                        subject_template_name="registration/password_reset_subject.txt",
                    )

            representante.user = user
            representante.save()

        messages.success(self.request, "Representante criado com sucesso como Associado.")
        return redirect(self.success_url)


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
            User = get_user_model()

            with transaction.atomic():
                representante = rep_form.save()

                user = User.objects.filter(email__iexact=representante.email).first()

                if user:
                    if getattr(user, "representante_profile", None):
                        messages.error(
                            request,
                            "Já existe um representante vinculado a este e-mail. "
                            "Entre em contato com a diretoria para ajustar o cadastro."
                        )
                        return render(
                            request,
                            self.template_name,
                            {"rep_form": rep_form, "company_form": company_form},
                        )

                    representante.user = user
                    representante.save(update_fields=["user"])

                else:
                    email = representante.email.strip().lower()

                    user = User.objects.create_user(username=email, email=email)

                    temp_password = secrets.token_urlsafe(16)
                    user.set_password(temp_password)
                    user.save(update_fields=["password"])

                    representante.user = user
                    representante.save(update_fields=["user"])

                    reset_form = PasswordResetForm({"email": user.email})
                    if reset_form.is_valid():
                        reset_form.save(
                            request=request,
                            use_https=request.is_secure(),
                            email_template_name="registration/password_reset_email.html",
                            subject_template_name="registration/password_reset_subject.txt",
                        )

                company = company_form.save(commit=False)
                company.representante = representante
                company.save()

            messages.success(
                request,
                "Empresa cadastrada com sucesso! "
                "Se o seu usuário ainda não existia, enviamos um link para você definir sua senha. "
                "Após análise, a diretoria liberará o acesso como Associado.",
            )
            return redirect("login")

        messages.error(request, "Corrija os campos destacados e tente novamente.")
        return render(
            request,
            self.template_name,
            {"rep_form": rep_form, "company_form": company_form},
        )


# ======================
# EXPORTS (Diretoria)
# ======================

@login_required
@user_passes_test(can_manage_companies, login_url="/accounts/home/")
def company_export_csv(request):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="relatorio_empresas.csv"'
    response.write("\ufeff".encode("utf8"))  # BOM pro Excel ler acentos

    writer = csv.writer(response, delimiter=";")
    writer.writerow(
        [
            "ID",
            "Nome Fantasia",
            "Razão Social",
            "CNPJ",
            "Área de Atuação",
            "Cidade/UF",
            "Email",
            "Telefone",
        ]
    )

    for company in Company.objects.all().order_by("nome_fantasia"):
        writer.writerow(
            [
                company.id,
                company.nome_fantasia,
                company.razao_social,
                company.cnpj,
                company.get_area_atuacao_display(),
                f"{company.cidade}/{company.estado}",
                company.email_contato,
                company.telefone,
            ]
        )

    return response


@login_required
@user_passes_test(can_manage_companies, login_url="/accounts/home/")
def company_export_pdf(request):
    companies = Company.objects.all().order_by("nome_fantasia")
    context = {"companies": companies, "title": "Relatório de Empresas"}

    template_path = "company/report_pdf.html"
    template = get_template(template_path)
    html = template.render(context)

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="relatorio_empresas.pdf"'

    pisa_status = pisa.CreatePDF(
        io.BytesIO(html.encode("UTF-8")),
        dest=response,
        encoding="UTF-8",
    )

    if pisa_status.err:
        return HttpResponse("Erro ao gerar PDF")

    return response
