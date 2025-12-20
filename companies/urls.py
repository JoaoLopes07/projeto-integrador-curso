from django.urls import path, include
from .views import CompanyListView, CompanyCreateView

urlpatterns = [
    path('', CompanyListView.as_view(), name='company-list'),
    path('novo/', CompanyCreateView.as_view(), name='company-create'),
    #path('<int:pk>/', CompanyUpdateView.as_view(), name='company-update'),
    #path('<int:pk>/delete/', CompanyDeleteView.as_view(), name='company-delete'),
]
