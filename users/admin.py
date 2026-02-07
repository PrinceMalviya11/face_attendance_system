"""
Admin configuration for User Profile
"""
from django.contrib import admin
from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """Admin interface for UserProfile"""
    list_display = ('user', 'face_dataset_collected', 'face_samples_count', 'last_dataset_update')
    list_filter = ('face_dataset_collected', 'created_at')
    search_fields = ('user__username', 'user__email', 'user__unique_id')
    readonly_fields = ('created_at', 'updated_at')
