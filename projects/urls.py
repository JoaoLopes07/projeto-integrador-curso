from django.urls import path
from .views import (
    ProjectListView,
    ProjectCreateView,
    ProjectDetailView,
    ProjectUpdateView,
    project_export_csv,
    project_export_pdf,
)

urlpatterns = [
    path("", ProjectListView.as_view(), name="project_list"),
    path("novo/", ProjectCreateView.as_view(), name="project_create"),
    path("<int:pk>/", ProjectDetailView.as_view(), name="project_detail"),
    path("<int:pk>/editar/", ProjectUpdateView.as_view(), name="project_update"),
    path("exportar/csv/", project_export_csv, name="project_export_csv"),
    path("exportar/pdf/", project_export_pdf, name="project_export_pdf"),
]
