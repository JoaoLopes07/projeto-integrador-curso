from django.urls import path
from django.shortcuts import redirect
from .views import survey_response_create, survey_already_answered, survey_success

app_name = "surveys"

urlpatterns = [
    path("", lambda request: redirect("surveys:responder"), name="index"),
    path("responder/", survey_response_create, name="responder"),
    path("ja-respondeu/", survey_already_answered, name="already_answered"),
    path("sucesso/", survey_success, name="success"),
]
