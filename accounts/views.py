from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test

#ferifica se é admin

def is_admin(user):
    """Verifica se o usuário é administrador"""
    return user.is_superuser  

#view_login

def login_view(request):
    """Página de login - pública"""
    
    if request.user.is_authenticated:
        # Verifique se 'home' existe ou use outro nome
        return redirect('home')
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, f'Bem-vindo, {username}!')
                return redirect('home')
            else:
                messages.error(request, 'Usuário ou senha inválidos.')
        else:
            messages.error(request, 'Usuário ou senha inválidos.')
    else:
        form = AuthenticationForm()
    
    return render(request, 'accounts/login.html', {'form': form})

#view publico

@login_required
def logout_view(request):

    """Logout - para todos os usuários logados"""

    username = request.user.username
    logout(request)
    messages.info(request, f'Até logo, {username}!')
    return redirect('login')

@login_required
def home_view(request):
    """Página inicial """

    return render(request, 'accounts/home.html', {'user': request.user})

@login_required
def profile_view(request):
    """Perfil do usuário """

    return render(request, 'accounts/profile.html', {'user': request.user})

#apenas para admin

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    """Dashboard administrativo """
    return render(request, 'accounts/admin_dashboard.html', {'user': request.user})

@login_required
@user_passes_test(is_admin)
def admin_settings(request):
    """Configurações do sistema """
    return render(request, 'accounts/admin_settings.html', {'user': request.user})