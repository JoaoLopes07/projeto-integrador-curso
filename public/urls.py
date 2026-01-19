from django.urls import path
from . import views

app_name = "public"

urlpatterns = [
    path("", views.landing, name="landing"),
    path("mapa/", views.map_view, name="mapa"),
    path("diretorio/", views.diretorio, name="diretorio"),
    path("estatisticas/", views.estatisticas, name="estatisticas"),
]
