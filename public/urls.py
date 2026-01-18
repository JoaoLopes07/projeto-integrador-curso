from django.urls import path
from .views import landing, map_view

app_name = "public"

urlpatterns = [
    path("", landing, name="landing"),
    path("mapa/", map_view, name="mapa"),
]
