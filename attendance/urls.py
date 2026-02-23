"""
URL Configuration for Attendance App
"""
from django.urls import path
from . import views

app_name = 'attendance'

urlpatterns = [
    path('mark/', views.mark_attendance_view, name='mark_attendance'),
    path('history/', views.attendance_history, name='attendance_history'),
    path('reports/daily/', views.daily_report, name='daily_report'),
    path('reports/monthly/', views.monthly_report, name='monthly_report'),
    path('reports/user/<int:user_id>/', views.user_report, name='user_report'),
    path('reports/send-email/', views.send_report_email, name='send_report_email'),
    path('reports/user-preview/', views.get_user_attendance_preview, name='user_attendance_preview'),
]
