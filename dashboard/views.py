"""
Dashboard Views
Admin and User dashboards with statistics
"""
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Count
from datetime import datetime, timedelta
from accounts.models import CustomUser
from accounts.decorators import admin_required, user_required
from attendance.models import Attendance
from face_recognition_app.models import FaceData
from users.models import UserProfile
import os
from django.conf import settings


@login_required
def index(request):
    """
    Main dashboard - redirects based on user role
    """
    if request.user.is_admin():
        return redirect('dashboard:admin_dashboard')
    else:
        return redirect('dashboard:user_dashboard')


@admin_required
def admin_dashboard(request):
    """
    Admin Dashboard with system statistics
    """
    
    # User statistics
    total_users = CustomUser.objects.count()
    admin_users = CustomUser.objects.filter(role='ADMIN').count()
    regular_users = CustomUser.objects.filter(role='USER').count()
    active_users = CustomUser.objects.filter(is_active=True).count()
    
    # Face dataset statistics
    users_with_face_data = FaceData.objects.filter(dataset_collected=True).count()
    users_without_face_data = total_users - users_with_face_data
    
    # Model status
    model_exists = os.path.exists(settings.FACE_MODEL_PATH)
    model_status = "Trained" if model_exists else "Not Trained"
    
    # Attendance statistics - use timezone-aware dates
    today = timezone.localtime(timezone.now()).date()
    today_attendance = Attendance.objects.filter(date=today).count()
    
    # This week attendance
    week_start = today - timedelta(days=today.weekday())
    week_attendance = Attendance.objects.filter(date__gte=week_start).count()
    
    # This month attendance
    month_start = today.replace(day=1)
    month_attendance = Attendance.objects.filter(date__gte=month_start).count()
    
    # Recent attendance records
    recent_attendance = Attendance.objects.all().select_related('user')[:10]
    
    # Users without face data
    users_needing_face_data = CustomUser.objects.exclude(
        id__in=FaceData.objects.filter(dataset_collected=True).values_list('user_id', flat=True)
    )[:5]
    
    context = {
        'total_users': total_users,
        'admin_users': admin_users,
        'regular_users': regular_users,
        'active_users': active_users,
        'users_with_face_data': users_with_face_data,
        'users_without_face_data': users_without_face_data,
        'model_status': model_status,
        'model_exists': model_exists,
        'today_attendance': today_attendance,
        'week_attendance': week_attendance,
        'month_attendance': month_attendance,
        'recent_attendance': recent_attendance,
        'users_needing_face_data': users_needing_face_data,
    }
    
    return render(request, 'dashboard/admin_dashboard.html', context)


@user_required
def user_dashboard(request):
    """
    User Dashboard with personal statistics
    """
    user = request.user
    
    # Get or create user profile
    profile, created = UserProfile.objects.get_or_create(user=user)
    
    # Face data status
    try:
        face_data = FaceData.objects.get(user=user)
        has_face_data = face_data.dataset_collected
        face_samples = face_data.samples_count
    except FaceData.DoesNotExist:
        has_face_data = False
        face_samples = 0
    
    # Attendance statistics - use timezone-aware dates
    total_attendance = Attendance.objects.filter(user=user).count()
    
    # This month attendance
    today = timezone.localtime(timezone.now()).date()
    month_start = today.replace(day=1)
    month_attendance = Attendance.objects.filter(user=user, date__gte=month_start).count()
    
    # This week attendance
    week_start = today - timedelta(days=today.weekday())
    week_attendance = Attendance.objects.filter(user=user, date__gte=week_start).count()
    
    # Recent attendance
    recent_attendance = Attendance.objects.filter(user=user)[:10]
    
    # Attendance percentage (assuming 30 days in a month)
    attendance_percentage = (month_attendance / 30) * 100 if month_attendance else 0
    
    context = {
        'profile': profile,
        'has_face_data': has_face_data,
        'face_samples': face_samples,
        'total_attendance': total_attendance,
        'month_attendance': month_attendance,
        'week_attendance': week_attendance,
        'recent_attendance': recent_attendance,
        'attendance_percentage': round(attendance_percentage, 2),
    }
    
    return render(request, 'dashboard/user_dashboard.html', context)


@login_required
def profile_view(request):
    """
    View and edit user profile
    """
    user = request.user
    profile, created = UserProfile.objects.get_or_create(user=user)
    
    context = {
        'user_obj': user,
        'profile': profile,
    }
    
    return render(request, 'dashboard/profile.html', context)
