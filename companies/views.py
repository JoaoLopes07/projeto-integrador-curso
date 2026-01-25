from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.core.exceptions import PermissionDenied
import secrets
from .models import Company, Representante
from .forms import CompanyForm, RepresentanteForm, RepresentantePublicForm, CompanyPublicForm
from core.permissions import can_view_company_data, can_manage_companies

from django.views import View
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import transaction


admin_required = [
    login_required,
    user_passes_test(can_view_company_data, login_url='/accounts/home/')
]


@method_decorator(admin_required, name='dispatch')
class CompanyListView(ListView):
    model = Company
    template_name = 'company/company_list.html'
    
    def get_queryset(self):
        user = self.request.user

        if can_manage_companies(user):  # diretoria pode ver todas
            return Company.objects.all()

        # associado:vê só as suas empresas
        return Company.objects.filter(representante__user=user)


@method_decorator([login_required, user_passes_test(can_manage_companies, login_url='/accounts/home/')], name='dispatch')
class CompanyCreateView(CreateView):
    model = Company
    form_class = CompanyForm
    template_name = 'company/company_form.html'
    success_url = reverse_lazy('company-list')


@method_decorator(admin_required, name='dispatch')
class CompanyUpdateView(UpdateView):
    model = Company
    form_class = CompanyForm
    template_name = 'company/company_form.html'
    success_url = reverse_lazy('company-list')
    
    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        user = self.request.user

        if can_manage_companies(user):  # diretoria pode editar todos
            return obj

        if obj.representante and obj.representante.user_id == user.id:
            return obj

        raise PermissionDenied("Você não tem permissão para editar esta empresa.")


@method_decorator(admin_required, name='dispatch')
class CompanyDeleteView(DeleteView):
    model = Company
    success_url = reverse_lazy('company-list')
    
    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        user = self.request.user

        if can_manage_companies(user):
            return obj

        if obj.representante and obj.representante.user_id == user.id:
            return obj

        raise PermissionDenied("Você não tem permissão para excluir esta empresa.")


@method_decorator(admin_required, name='dispatch')
class RepresentanteListView(ListView):
    model = Representante
    template_name = 'representante/representante_list.html'


@method_decorator(admin_required, name='dispatch')
class RepresentanteCreateView(CreateView):
    model = Representante
    form_class = RepresentanteForm
    template_name = 'representante/representante_form.html'
    success_url = reverse_lazy('representante-list')
    
    
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
                    
                user = User.objects.create_user(
                    username=email,
                    email=email,
                )
                
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

        messages.success(self.request,"Representante criado com sucesso como Associado.")
        return redirect(self.success_url)     

@method_decorator(admin_required, name='dispatch')
class RepresentanteUpdateView(UpdateView):
    model = Representante
    form_class = RepresentanteForm
    template_name = 'representante/representante_form.html'
    success_url = reverse_lazy('representante-list')


@method_decorator(admin_required, name='dispatch')
class RepresentanteDeleteView(DeleteView):
    model = Representante
    success_url = reverse_lazy('representante-list')


class CompanyPublicRegisterView(View):
    template_name = "company/company_public_register.html"

    def get(self, request):
        return render(request, self.template_name, {
            "rep_form": RepresentantePublicForm(),
            "company_form": CompanyPublicForm(),
        })

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
                        return render(request, self.template_name, {
                                "rep_form": rep_form,
                                "company_form": company_form,
                            })

                    representante.user = user
                    representante.save(update_fields=["user"])

                else:
                    # Se não existir, cria usuário 
                    
                    email = representante.email.strip().lower()
                    
                    user = User.objects.create_user(
                        username=email,
                        email=email,  
                    )
                    
                    temp_password = secrets.token_urlsafe(16)
                    user.set_password(temp_password)
                    user.save(update_fields=["password"])


                    # Vincula o representante ao user recém-criado
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
                "Se o seu usuário ainda não existia, enviamos um link para você definir sua senha."
                "Após análise, a diretoria liberará o acesso como Associado."
            )
            return redirect("login")

        messages.error(request, "Corrija os campos destacados e tente novamente.")
        return render(request, self.template_name, {
            "rep_form": rep_form,
            "company_form": company_form,
        })