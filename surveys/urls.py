from django.urls import path
from django.shortcuts import redirect
from .views import (
    survey_response_create,
    survey_already_answered,
    survey_success,
    survey_history,
    survey_public_report,
    survey_export_csv,
    survey_export_pdf,
)

app_name = "surveys"

urlpatterns = [
    path("", lambda request: redirect("surveys:responder"), name="index"),
    path("responder/", survey_response_create, name="responder"),
    path("ja-respondeu/", survey_already_answered, name="already_answered"),
    path("sucesso/", survey_success, name="success"),
    path("historico/", survey_history, name="history"),
    path("relatorios/", survey_public_report, name="report_public"),
    path("relatorios/exportar/", survey_export_csv, name="export_csv"),
    path("export/pdf/", survey_export_pdf, name="export_pdf"),
]
