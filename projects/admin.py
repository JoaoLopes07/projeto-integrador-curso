from django.contrib import admin
from .models import (
    Project,
    ProjectLink,
    ProjectMember,
    ProjectImage
)


class ProjectLinkInline(admin.TabularInline):
    model = ProjectLink
    extra = 1


class ProjectMemberInline(admin.TabularInline):
    model = ProjectMember
    extra = 1


class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'company', 'created_at')
    list_filter = ('status', 'company')
    search_fields = ('name',)
    inlines = [
        ProjectLinkInline,
        ProjectMemberInline,
        ProjectImageInline
    ]
