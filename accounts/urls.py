from django.urls import path
from . import views

urlpatterns = [
    # Público
    path('login/', views.login_view, name='login'),
    
    # Para todos logados (membros e admins)
    path('logout/', views.logout_view, name='logout'),
    path('home/', views.home_view, name='home'),
    path('profile/', views.profile_view, name='profile'),
    
    # Exclusivo para administradores
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/settings/', views.admin_settings, name='admin_settings'),
]