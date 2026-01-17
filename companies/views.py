from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Company, Representante
from .forms import CompanyForm, RepresentanteForm
from core.permissions import can_manage_companies


admin_required = [
    login_required,
    user_passes_test(can_manage_companies, login_url='/accounts/home/')
]


@method_decorator(admin_required, name='dispatch')
class CompanyListView(ListView):
    model = Company
    template_name = 'company/company_list.html'


@method_decorator(admin_required, name='dispatch')
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


@method_decorator(admin_required, name='dispatch')
class CompanyDeleteView(DeleteView):
    model = Company
    success_url = reverse_lazy('company-list')


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
