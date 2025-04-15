from django.contrib import admin

from .models import Chat, Project, ProjectFile


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at", "updated_at", "is_deleted")
    list_filter = ("is_deleted", "created_at")
    search_fields = ("name", "description")


@admin.register(ProjectFile)
class ProjectFileAdmin(admin.ModelAdmin):
    list_display = ("name", "project", "file_type", "size", "created_at")
    list_filter = ("file_type", "created_at", "is_deleted")
    search_fields = ("name", "project__name")


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = ("project", "created_at", "is_deleted")
    list_filter = ("created_at", "is_deleted")
    search_fields = ("message", "response")
    list_filter = ("created_at", "is_deleted")
    search_fields = ("message", "response")
