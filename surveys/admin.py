from django.contrib import admin
from .models import SurveyYear, SurveyResponse


@admin.register(SurveyYear)
class SurveyYearAdmin(admin.ModelAdmin):
    list_display = ("year", "is_active", "created_at")
    list_filter = ("is_active",)
    search_fields = ("year",)


@admin.register(SurveyResponse)
class SurveyResponseAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "survey_year",
        "submitted_at",
    )
    list_filter = ("survey_year",)
    search_fields = ("user__username",)
