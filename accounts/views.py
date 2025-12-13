# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import CustomUser

def is_admin(user):
    """Verifica se o usuário é administrador"""
    return user.is_superuser  

@login_required
def home_view(request):
    """Página inicial - redireciona admin para dashboard"""
    if request.user.is_superuser:
        return redirect('admin_dashboard')
    
    return render(request, 'accounts/home.html', {'user': request.user})

@login_required
def profile_view(request):
    """Perfil do usuário"""
    return render(request, 'accounts/profile.html', {'user': request.user})

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    """Dashboard administrativo"""
    users = CustomUser.objects.all().order_by('-date_joined')
    return render(request, 'accounts/admin_dashboard.html', {
        'user': request.user,
        'users': users
    })

@login_required
@user_passes_test(is_admin)
def admin_settings(request):
    """Configurações do sistema"""
    return render(request, 'accounts/admin_settings.html', {'user': request.user})