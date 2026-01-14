from django.urls import path
from . import views  #  Importando as views do app accounts

urlpatterns = [
    
    # Público
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    
    # Para todos logados
    path('logout/', views.logout_view, name='logout'),
    path('home/', views.home_view, name='home'),
    path('profile/', views.profile_view, name='profile'),

    # Exclusivo para administradores
    path('admin/', views.admin_dashboard, name='admin_profile'),
    path('admin/settings/', views.admin_settings, name='admin_settings'),
]