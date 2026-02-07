"""
Admin configuration for Attendance
"""
from django.contrib import admin
from .models import Attendance


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    """Admin interface for Attendance"""
    list_display = ('user', 'date', 'time', 'status', 'subject', 'session', 'confidence')
    list_filter = ('status', 'date', 'subject', 'session')
    search_fields = ('user__username', 'user__email', 'user__unique_id', 'subject', 'session')
    date_hierarchy = 'date'
    readonly_fields = ('created_at',)
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('user')
