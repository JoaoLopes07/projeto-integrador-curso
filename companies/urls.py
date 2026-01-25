from django.urls import path
from .views import (
    CompanyListView,
    CompanyCreateView,
    CompanyUpdateView,
    CompanyDeleteView,
    RepresentanteListView,
    RepresentanteCreateView,
    RepresentanteUpdateView,
    RepresentanteDeleteView,
    CompanyPublicRegisterView,
    company_export_csv,
    company_export_pdf,
)

urlpatterns = [
    path("", CompanyListView.as_view(), name="company-list"),
    path(
        "cadastrar/",
        CompanyPublicRegisterView.as_view(),
        name="company-public-register",
    ),
    path("novo/", CompanyCreateView.as_view(), name="company-create"),
    path("<int:pk>/editar/", CompanyUpdateView.as_view(), name="company-update"),
    path("<int:pk>/deletar/", CompanyDeleteView.as_view(), name="company-delete"),
    path("representantes/", RepresentanteListView.as_view(), name="representante-list"),
    path(
        "representantes/novo/",
        RepresentanteCreateView.as_view(),
        name="representante-create",
    ),
    path(
        "representantes/<int:pk>/editar/",
        RepresentanteUpdateView.as_view(),
        name="representante-update",
    ),
    path(
        "representantes/<int:pk>/deletar/",
        RepresentanteDeleteView.as_view(),
        name="representante-delete",
    ),
    path("exportar/csv/", company_export_csv, name="company-export-csv"),
    path("exportar/pdf/", company_export_pdf, name="company-export-pdf"),
]
