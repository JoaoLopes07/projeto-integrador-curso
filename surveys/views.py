from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from .models import SurveyYear, SurveyResponse
from .forms import SurveyResponseForm, SurveyResponseAfiliadoForm


@login_required
def survey_response_create(request):
    # 1) Busca o ano ativo
    survey_year = SurveyYear.objects.filter(is_active=True).first()
    if not survey_year:
        messages.error(request, "Não há pesquisa ativa no momento.")
        return redirect("home")

    # 2) Permissão por role (apenas os permitidos respondem)
    if request.user.role not in ["diretoria", "associado", "afiliado"]:
        messages.error(request, "Seu perfil não pode responder a Pesquisa Socioeconômica Anual.")
        return redirect("home")

    # 3) Verifica se o usuário já respondeu
    if SurveyResponse.objects.filter(user=request.user, survey_year=survey_year).exists():
        messages.warning(request, "Você já respondeu a pesquisa deste ano.")
        return redirect("surveys:already_answered")
    
    if request.user.role in ["diretoria", "associado"]:
        FormClass = SurveyResponseForm
    else:  
        FormClass = SurveyResponseAfiliadoForm



    # 4). Processa formulário e salva resposta
    if request.method == "POST":
        form = FormClass(request.POST)
        if form.is_valid():
            response = form.save(commit=False)
            response.user = request.user
            response.survey_year = survey_year
            response.save()

            messages.success(
                request,
                "Pesquisa enviada com sucesso!"
            )
            return redirect("surveys:success")

    else:
        form = FormClass()

    return render(
        request,
        "surveys/survey_form.html",
        {"form": form, "survey_year": survey_year}
    )

@login_required
def survey_already_answered(request):
    return render(
        request,
        "surveys/already_answered.html"
    )


@login_required
def survey_success(request):
    return render(
        request,
        "surveys/success.html"
    )
