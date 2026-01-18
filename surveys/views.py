from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.db.models import Count
import csv

from .models import SurveyYear, SurveyResponse
from .forms import SurveyResponseForm, SurveyResponseAfiliadoForm

def is_diretoria(user):
    return user.is_authenticated and getattr(user, "role", None) == "diretoria"


def can_fill_survey(user):
    return user.is_authenticated and getattr(user, "role", None) in ["diretoria", "associado", "afiliado"]


def can_view_aggregated_reports(user):
    
    if not user.is_authenticated:
        return True  # público
    return getattr(user, "role", None) in ["diretoria", "coletivo"]


def get_active_year():
    return SurveyYear.objects.filter(is_active=True).first()

def get_public_aggregates(survey_year: SurveyYear):
   
    qs = SurveyResponse.objects.filter(survey_year=survey_year)

    total_respostas = qs.count()

    porte = (
        qs.exclude(company_size__isnull=True)
          .exclude(company_size__exact="")
          .values("company_size")
          .annotate(total=Count("id"))
          .order_by("-total")
    )

    faturamento = (
        qs.exclude(annual_revenue__isnull=True)
          .exclude(annual_revenue__exact="")
          .values("annual_revenue")
          .annotate(total=Count("id"))
          .order_by("-total")
    )

    total_com_dificuldade = qs.exclude(main_difficulty__isnull=True).exclude(main_difficulty__exact="").count()

    return {
        "year": survey_year.year,
        "total_respostas": total_respostas,
        "distribuicao_porte": list(porte),
        "distribuicao_faturamento": list(faturamento),
        "total_com_dificuldade": total_com_dificuldade,
    }

@login_required
def survey_response_create(request):
    # 1) Busca o ano ativo
    survey_year = get_active_year()
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
    
    
@login_required
def survey_history(request):
    role = getattr(request.user, "role", None)

    if role == "coletivo":
        messages.error(request, "Seu perfil não possui histórico de respostas (apenas relatórios agregados).")
        return redirect("home")

    qs = SurveyResponse.objects.select_related("survey_year", "user").order_by("-survey_year__year", "-submitted_at")

    if role != "diretoria":
        qs = qs.filter(user=request.user)

    return render(request, "surveys/history.html", {"responses": qs})

def survey_public_report(request):
    if not can_view_aggregated_reports(request.user):
        messages.error(request, "Você não tem permissão para acessar relatórios.")
        return redirect("home")

    
    year_param = request.GET.get("year")
    if year_param:
        survey_year = SurveyYear.objects.filter(year=year_param).first()
    else:
        survey_year = get_active_year()

    if not survey_year:
        messages.error(request, "Não há pesquisa ativa no momento.")
        return redirect("home")

    data = get_public_aggregates(survey_year)

    # Esse flag permite no template mostrar botões/filtros extras para coletivo/diretoria
    can_use_tools = request.user.is_authenticated and getattr(request.user, "role", None) in ["diretoria", "coletivo"]

    return render(
        request,
        "surveys/report_public.html",
        {
            "report": data,
            "survey_year": survey_year,
            "can_use_tools": can_use_tools,
            "available_years": SurveyYear.objects.all(),
        },
    )
    
@login_required
def survey_export_csv(request):
    if not is_diretoria(request.user):
        messages.error(request, "Apenas a diretoria pode exportar relatórios.")
        return redirect("home")

    year_param = request.GET.get("year")
    if year_param:
        survey_year = SurveyYear.objects.filter(year=year_param).first()
    else:
        survey_year = get_active_year()

    if not survey_year:
        messages.error(request, "Não há pesquisa ativa no momento.")
        return redirect("home")

    qs = (
        SurveyResponse.objects
        .select_related("user", "survey_year")
        .filter(survey_year=survey_year)
        .order_by("-submitted_at")
    )

    response = HttpResponse(content_type="text/csv; charset=utf-8")
    response["Content-Disposition"] = f'attachment; filename="pesquisa_{survey_year.year}.csv"'

    writer = csv.writer(response)
    writer.writerow([
        "ano",
        "data_envio",
        "usuario_email",
        "usuario_role",
        "company_size",
        "annual_revenue",
        "main_difficulty",
    ])

    for r in qs:
        writer.writerow([
            r.survey_year.year,
            r.submitted_at.strftime("%Y-%m-%d %H:%M:%S"),
            getattr(r.user, "email", ""),
            getattr(r.user, "role", ""),
            r.company_size or "",
            r.annual_revenue or "",
            r.main_difficulty or "",
        ])

    return response    
    
