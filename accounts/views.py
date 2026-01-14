from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib import messages
from django.utils.http import url_has_allowed_host_and_scheme
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required, user_passes_test

def login_view(request):
    """Página de login - pública"""
    
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('/admin/')
        return redirect('home')
    
    next_url = request.GET.get('next', '')
    
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, f'Bem-vindo, {username}!')
                
                next_post = request.POST.get('next', '')
                redirect_url = next_post or next_url
                
                if redirect_url and url_has_allowed_host_and_scheme(
                    redirect_url, 
                    allowed_hosts={request.get_host()}
                ):
                    return redirect(redirect_url)
                
                if user.is_superuser:
                    return redirect('/admin/')
                else:
                    return redirect('home')
            else:
                messages.error(request, 'Usuário ou senha inválidos.')
        else:
            messages.error(request, 'Usuário ou senha inválidos.')
    else:
        form = AuthenticationForm()
    
    return render(request, 'accounts/login.html', {
        'form': form,
        'next': next_url
    })

def register_view(request):
    """View para registro de novos usuários"""
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('admin_profile')
        return redirect('home')
    
    if request.method == 'POST':
        
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Conta criada com sucesso! Bem-vindo, {user.username}!')
            
            if user.is_superuser:
                return redirect('admin_profile')
            return redirect('home')
        else:
            
            # Exiba os erros específicos do formulário
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'accounts/register.html', {'form': form})

def logout_view(request):
    """Logout - para todos os usuários logados"""
    username = request.user.username
    logout(request)
    messages.info(request, f'Até logo, {username}!')
    return redirect('login')

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


