from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import CustomUser

def is_admin(user):
    """Verifica se o usuário é administrador"""
    return user.is_superuser  

@login_required
def home_view(request):
    """Página inicial """
    if request.user.is_superuser:
        return redirect('admin_profile')
    
    return render(request, 'accounts/home.html', {'user': request.user})

@login_required
def profile_view(request):
    """Perfil do usuário"""
    return render(request, 'accounts/profile.html', {'user': request.user})

