from django.contrib import admin
from .models import Project

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'company', 'created_at')
    list_filter = ('status', 'company')
    search_fields = ('name',)
