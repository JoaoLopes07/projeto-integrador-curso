from django.urls import path, include
from .views import CompanyListView, CompanyCreateView, RepresentanteListView, RepresentanteCreateView, CompanyUpdateView, RepresentanteUpdateView, CompanyDeleteView, RepresentanteDeleteView

urlpatterns = [
    path('', CompanyListView.as_view(), name='company-list'),
    path('novo/', CompanyCreateView.as_view(), name='company-create'),
    path('representantes/', RepresentanteListView.as_view(), name='representante-list'),
    path('representantes/novo/', RepresentanteCreateView.as_view(), name='representante-create'),
    path('<int:pk>/editar/', CompanyUpdateView.as_view(), name='company-update'),
    path('representantes/<int:pk>/editar/', RepresentanteUpdateView.as_view(), name='representante-update'),
    path('<int:pk>/deletar/', CompanyDeleteView.as_view(), name='company-delete'),
    path('representantes/<int:pk>/deletar/', RepresentanteDeleteView.as_view(), name='representante-delete'),
]
