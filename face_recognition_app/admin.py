"""
Admin configuration for Face Recognition App
"""
from django.contrib import admin
from .models import FaceData


@admin.register(FaceData)
class FaceDataAdmin(admin.ModelAdmin):
    """Admin interface for FaceData"""
    list_display = ('user', 'dataset_collected', 'samples_count', 'last_updated')
    list_filter = ('dataset_collected', 'created_at')
    search_fields = ('user__username', 'user__email', 'user__unique_id')
    readonly_fields = ('created_at', 'last_updated')
