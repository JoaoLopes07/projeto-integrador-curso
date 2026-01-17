from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.utils.http import url_has_allowed_host_and_scheme
from .forms import CustomUserCreationForm

REDIRECT_URL = "/redirect/" 

def login_view(request):
    if request.user.is_authenticated:
        return redirect(REDIRECT_URL)

    next_url = request.GET.get("next")
    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        login(request, user)
        messages.success(request, f"Bem-vindo, {user.username}!")

        if next_url and url_has_allowed_host_and_scheme(next_url, {request.get_host()}):
            return redirect(next_url)

        return redirect(REDIRECT_URL)

    return render(request, "accounts/login.html", {"form": form, "next": next_url})

def register_view(request):
    if request.user.is_authenticated:
        return redirect(REDIRECT_URL)

    form = CustomUserCreationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, "Conta criada com sucesso!")
        return redirect(REDIRECT_URL)

    return render(request, "accounts/register.html", {"form": form})

@login_required
def logout_view(request):
    logout(request)
    messages.info(request, "Você saiu do sistema.")
    return redirect("login")

@login_required
def home_view(request):
    return render(request, "accounts/home.html")

@login_required
def profile_view(request):
    return render(request, "accounts/profile.html")
