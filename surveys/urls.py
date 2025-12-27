from django.urls import path
from .views import survey_response_create

urlpatterns = [
    path("responder/", survey_response_create, name="survey_response"),
]
