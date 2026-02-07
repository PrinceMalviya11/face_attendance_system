"""
Attendance Views
Handles attendance marking, viewing, and report generation
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.db.models import Count, Q
from datetime import datetime, timedelta
from accounts.models import CustomUser
from .models import Attendance
from .reports import (
    generate_csv_report, generate_excel_report, send_attendance_report_email,
    get_daily_report, get_monthly_report, get_user_report, get_date_range_report
)
from face_recognition_app.face_utils import face_recognition_system


@login_required
@csrf_exempt
def mark_attendance_view(request):
    """
    Mark attendance using face recognition
    """
    if request.method == 'POST':
        import cv2
        
        # Capture frame from webcam
        camera = cv2.VideoCapture(0)
        ret, frame = camera.read()
        camera.release()
        
        if not ret:
            return JsonResponse({
                'success': False,
                'message': 'Failed to capture frame from webcam'
            })
        
        # Recognize face
        user_id, confidence, face_location = face_recognition_system.recognize_face(frame)
        
        if user_id is not None:
            try:
                user = CustomUser.objects.get(id=user_id)
                
                # Get session from request
                subject = request.POST.get('subject', '')
                session = request.POST.get('session', 'Default')
                
                # Mark attendance
                attendance, created = Attendance.mark_attendance(
                    user=user,
                    subject=subject,
                    session=session,
                    confidence=confidence
                )
                
                if created:
                    return JsonResponse({
                        'success': True,
                        'message': f'Attendance marked for {user.first_name} {user.last_name}',
                        'user': {
                            'username': user.username,
                            'unique_id': user.unique_id,
                            'full_name': f"{user.first_name} {user.last_name}",
                        },
                        'attendance': {
                            'date': str(attendance.date),
                            'time': str(attendance.time),
                            'status': attendance.status,
                        }
                    })
                else:
                    return JsonResponse({
                        'success': False,
                        'message': f'Attendance already marked for {user.first_name} {user.last_name} today',
                        'user': {
                            'username': user.username,
                            'unique_id': user.unique_id,
                            'full_name': f"{user.first_name} {user.last_name}",
                        }
                    })
            except CustomUser.DoesNotExist:
                return JsonResponse({
                    'success': False,
                    'message': 'User not found in database'
                })
        else:
            return JsonResponse({
                'success': False,
                'message': 'Face not recognized. Please try again.',
                'confidence': float(confidence) if confidence else None
            })
    
    return render(request, 'attendance/mark_attendance.html')


@login_required
def attendance_history(request):
    """
    View attendance history
    Users see their own history, Admins see all
    """
    if request.user.is_admin():
        attendances = Attendance.objects.all().select_related('user')
    else:
        attendances = Attendance.objects.filter(user=request.user)
    
    # Filter by date range if provided
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    
    if start_date:
        attendances = attendances.filter(date__gte=start_date)
    if end_date:
        attendances = attendances.filter(date__lte=end_date)
    
    context = {
        'attendances': attendances[:100],  # Limit to 100 records
        'start_date': start_date,
        'end_date': end_date,
    }
    
    return render(request, 'attendance/attendance_history.html', context)


@login_required
def daily_report(request):
    """
    Generate daily attendance report
    """
    if not request.user.is_admin():
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('dashboard:index')
    
    date_str = request.GET.get('date')
    if date_str:
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
    else:
        date = timezone.localtime(timezone.now()).date()
    
    attendances = get_daily_report(date)
    
    # Export options
    export_format = request.GET.get('export')
    if export_format == 'csv':
        return generate_csv_report(attendances, f'daily_report_{date}.csv')
    elif export_format == 'excel':
        return generate_excel_report(attendances, f'daily_report_{date}.xls')
    
    context = {
        'attendances': attendances,
        'date': date,
        'today': timezone.localtime(timezone.now()).date(),
        'total_present': attendances.filter(status='PRESENT').count(),
        'total_absent': attendances.filter(status='ABSENT').count(),
    }
    
    return render(request, 'attendance/daily_report.html', context)


@login_required
def monthly_report(request):
    """
    Generate monthly attendance report
    """
    if not request.user.is_admin():
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('dashboard:index')
    
    year = request.GET.get('year', timezone.now().year)
    month = request.GET.get('month', timezone.now().month)
    
    try:
        year = int(year)
        month = int(month)
    except ValueError:
        year = timezone.now().year
        month = timezone.now().month
    
    attendances = get_monthly_report(year, month)
    
    # Export options
    export_format = request.GET.get('export')
    if export_format == 'csv':
        return generate_csv_report(attendances, f'monthly_report_{year}_{month}.csv')
    elif export_format == 'excel':
        return generate_excel_report(attendances, f'monthly_report_{year}_{month}.xls')
    
    context = {
        'attendances': attendances,
        'year': year,
        'month': month,
        'total_present': attendances.filter(status='PRESENT').count(),
    }
    
    return render(request, 'attendance/monthly_report.html', context)


@login_required
def user_report(request, user_id=None):
    """
    Generate user-wise attendance report
    """
    if user_id is None:
        user_id = request.user.id
    
    # Check permissions
    if not request.user.is_admin() and request.user.id != user_id:
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('dashboard:index')
    
    user = get_object_or_404(CustomUser, id=user_id)
    
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    
    attendances = get_user_report(user_id, start_date, end_date)
    
    # Export options
    export_format = request.GET.get('export')
    if export_format == 'csv':
        return generate_csv_report(attendances, f'user_report_{user.username}.csv')
    elif export_format == 'excel':
        return generate_excel_report(attendances, f'user_report_{user.username}.xls')
    
    context = {
        'user_obj': user,
        'attendances': attendances,
        'start_date': start_date,
        'end_date': end_date,
        'total_present': attendances.filter(status='PRESENT').count(),
    }
    
    return render(request, 'attendance/user_report.html', context)


@login_required
def send_report_email(request):
    """
    Send attendance report via email
    """
    if not request.user.is_admin():
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('dashboard:index')
    
    if request.method == 'POST':
        email = request.POST.get('email')
        report_type = request.POST.get('report_type')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        
        # Validate required fields
        if not email or not report_type:
            messages.error(request, 'Email and report type are required.')
            return redirect('attendance:send_report_email')
        
        # Get attendances based on report type
        try:
            if report_type == 'daily':
                if not start_date:
                    messages.error(request, 'Please select a date for the daily report.')
                    return redirect('attendance:send_report_email')
                date = datetime.strptime(start_date, '%Y-%m-%d').date()
                attendances = get_daily_report(date)
                # For daily report, start and end date are the same
                end_date = start_date
            elif report_type == 'monthly':
                if not start_date:
                    messages.error(request, 'Please select a month for the monthly report.')
                    return redirect('attendance:send_report_email')

                try:
                    year, month = map(int, start_date.split('-')[:2])
                except ValueError:
                    messages.error(request, 'Invalid month format.')
                    return redirect('attendance:send_report_email')

                attendances = get_monthly_report(year, month)

                from calendar import monthrange
                last_day = monthrange(year, month)[1]

                start_date = f"{year}-{month:02d}-01"
                end_date = f"{year}-{month:02d}-{last_day}"

            else:  # custom
                if not start_date or not end_date:
                    messages.error(request, 'Please select both start and end dates for custom report.')
                    return redirect('attendance:send_report_email')
                attendances = get_date_range_report(start_date, end_date)
        except (ValueError, IndexError) as e:
            messages.error(request, f'Invalid date format: {str(e)}')
            return redirect('attendance:send_report_email')
        
        # Send email
        success = send_attendance_report_email(
            user_email=email,
            report_type=report_type,
            start_date=start_date,
            end_date=end_date,
            attendances=attendances
        )
        
        if success:
            messages.success(request, f'Report sent successfully to {email}')
        else:
            messages.error(request, 'Failed to send email. Please check email configuration.')
        
        return redirect('dashboard:admin_dashboard')
    
    return render(request, 'attendance/send_report.html')
