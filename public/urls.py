from django.urls import path
from .views import landing

app_name = "public"

urlpatterns = [
    path("", landing, name="landing"),
]
 