from django.conf import settings
from django.db import models


class SurveyYear(models.Model):
    year = models.PositiveIntegerField(unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-year"]

    def __str__(self):
        return f"Pesquisa {self.year}"


class SurveyResponse(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="survey_responses"
    )
    survey_year = models.ForeignKey(
        SurveyYear,
        on_delete=models.CASCADE,
        related_name="responses"
    )

    # Campos iniciais da pesquisa (podem evoluir depois)
    company_size = models.CharField(
        max_length=100,
        verbose_name="Porte da empresa"
    )
    annual_revenue = models.CharField(
        max_length=100,
        verbose_name="Faturamento anual"
    )
    main_difficulty = models.TextField(
        verbose_name="Principal dificuldade enfrentada"
    )

    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "survey_year"],
                name="unique_user_survey_year"
            )
        ]

    def __str__(self):
        return f"{self.user} - {self.survey_year.year}"
