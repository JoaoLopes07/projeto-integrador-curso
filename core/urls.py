from django.urls import path
from .views import redirect_after_login, dashboard_diretoria

urlpatterns = [
    path("", redirect_after_login, name="redirect_after_login"),
    path("diretoria/", dashboard_diretoria, name="dashboard_diretoria"),
]
