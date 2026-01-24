from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, update_session_auth_hash, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib import messages
from django.urls import reverse_lazy

from projects.models import Project
from .forms import CustomUserCreationForm, ProfileForm
from companies.models import Company

User = get_user_model()
REDIRECT_URL = reverse_lazy("home")  # Redireciona corretamente para /accounts/home/


def login_view(request):
    if request.user.is_authenticated:
        return redirect(REDIRECT_URL)

    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == "POST" and form.is_valid():
        login(request, form.get_user())
        messages.success(request, "Login realizado com sucesso.")
        return redirect(REDIRECT_URL)

    return render(request, "accounts/login.html", {"form": form})


def register_view(request):
    if request.user.is_authenticated:
        return redirect(REDIRECT_URL)

    form = CustomUserCreationForm(request.POST or None)

    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            if User.objects.filter(email=email).exists():
                form.add_error("email", "Este email já está em uso.")
            else:
                user = form.save()
                login(request, user)
                messages.success(request, "Conta criada com sucesso.")
                return redirect(REDIRECT_URL)

    return render(request, "accounts/register.html", {"form": form})


@login_required
def logout_view(request):
    logout(request)
    return redirect("login")


@login_required
def home_view(request):
    total_empresas = Company.objects.count()
    total_membros = User.objects.filter(is_active=True).count()

    total_projetos = Project.objects.count()
    projetos_andamento = Project.objects.filter(status='active').count()
    
    return render(request, "accounts/home.html", {
        'total_empresas': total_empresas,
        'total_membros': total_membros,
        'total_projetos': total_projetos,
        'projetos_andamento': projetos_andamento,
    })

@login_required
def profile_view(request):
    user = request.user
    has_company = Company.objects.filter(representante__email=user.email).exists()

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Perfil atualizado com sucesso.")
            return redirect("profile")
    else:
        form = ProfileForm(instance=user)

    return render(
        request,
        "accounts/profile.html",
        {
            "form": form,
            "has_company": has_company,
        }
    )


@login_required
def change_password_view(request):
    if request.method == "POST":
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Senha alterada com sucesso.")
            return redirect("profile")
    else:
        form = PasswordChangeForm(user=request.user)

    return render(request, "accounts/change_password.html", {"form": form})
