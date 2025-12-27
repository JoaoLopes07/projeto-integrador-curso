from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from .models import SurveyYear, SurveyResponse
from .forms import SurveyResponseForm


@login_required
def survey_response_create(request):
    # 1. Busca o ano ativo
    survey_year = get_object_or_404(SurveyYear, is_active=True)

    # 2. Verifica se o usuário já respondeu
    if SurveyResponse.objects.filter(
        user=request.user,
        survey_year=survey_year
    ).exists():
        messages.warning(
            request,
            "Você já respondeu a pesquisa deste ano."
        )
        return redirect("survey_already_answered")

    # 3. Processa formulário
    if request.method == "POST":
        form = SurveyResponseForm(request.POST)
        if form.is_valid():
            response = form.save(commit=False)
            response.user = request.user
            response.survey_year = survey_year
            response.save()

            messages.success(
                request,
                "Pesquisa enviada com sucesso!"
            )
            return redirect("survey_success")
    else:
        form = SurveyResponseForm()

    return render(
        request,
        "surveys/survey_form.html",
        {"form": form, "survey_year": survey_year}
    )
