"""
Attendance Report Generation
Handles CSV/Excel/PDF export and email delivery
"""
import csv
import xlwt
from io import BytesIO
from django.http import HttpResponse
from django.core.mail import EmailMessage
from django.conf import settings
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Attendance
from accounts.models import CustomUser

# PDF generation imports
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT


def generate_csv_report(attendances, filename="attendance_report.csv"):
    """
    Generate CSV report from attendance records
    
    Args:
        attendances: QuerySet of Attendance objects
        filename: Output filename
    
    Returns:
        HttpResponse with CSV file
    """
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    
    writer = csv.writer(response)
    writer.writerow(['User ID', 'Username', 'Name', 'Date', 'Time', 'Status', 'Subject', 'Session'])
    
    for attendance in attendances:
        writer.writerow([
            attendance.user.unique_id,
            attendance.user.username,
            f"{attendance.user.first_name} {attendance.user.last_name}",
            attendance.date,
            attendance.time,
            attendance.status,
            attendance.subject or '',
            attendance.session or '',
        ])
    
    return response


def generate_excel_report(attendances, filename="attendance_report.xls"):
    """
    Generate Excel report from attendance records
    
    Args:
        attendances: QuerySet of Attendance objects
        filename: Output filename
    
    Returns:
        HttpResponse with Excel file
    """
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Attendance Report')
    
    # Header style
    header_style = xlwt.easyxf('font: bold on; align: horiz center')
    
    # Write headers
    headers = ['User ID', 'Username', 'Name', 'Date', 'Time', 'Status', 'Subject', 'Session']
    for col, header in enumerate(headers):
        ws.write(0, col, header, header_style)
    
    # Write data
    for row, attendance in enumerate(attendances, start=1):
        ws.write(row, 0, attendance.user.unique_id)
        ws.write(row, 1, attendance.user.username)
        ws.write(row, 2, f"{attendance.user.first_name} {attendance.user.last_name}")
        ws.write(row, 3, str(attendance.date))
        ws.write(row, 4, str(attendance.time))
        ws.write(row, 5, attendance.status)
        ws.write(row, 6, attendance.subject or '')
        ws.write(row, 7, attendance.session or '')
    
    wb.save(response)
    return response


def send_attendance_report_email(user_email, report_type, start_date, end_date, attendances):
    """
    Send attendance report via email with PDF attachment
    
    Args:
        user_email: Recipient email address
        report_type: Type of report (daily, monthly, user-wise)
        start_date: Report start date
        end_date: Report end date
        attendances: QuerySet of Attendance objects
    
    Returns:
        bool: True if email sent successfully
    """
    try:
        # Create PDF in memory
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=0.5*inch, bottomMargin=0.5*inch)
        
        # Container for PDF elements
        elements = []
        
        # Styles
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=18,
            textColor=colors.HexColor('#1a237e'),
            spaceAfter=12,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        
        subtitle_style = ParagraphStyle(
            'CustomSubtitle',
            parent=styles['Normal'],
            fontSize=12,
            textColor=colors.HexColor('#424242'),
            spaceAfter=20,
            alignment=TA_CENTER,
            fontName='Helvetica'
        )
        
        # Add title
        title = Paragraph(f"Attendance Report - {report_type.title()}", title_style)
        elements.append(title)
        
        # Add subtitle with date range
        subtitle = Paragraph(f"Period: {start_date} to {end_date}", subtitle_style)
        elements.append(subtitle)
        
        # Add summary information
        summary_style = ParagraphStyle(
            'Summary',
            parent=styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#424242'),
            spaceAfter=15,
            alignment=TA_LEFT,
            fontName='Helvetica'
        )
        
        total_records = attendances.count()
        summary_text = f"<b>Total Records:</b> {total_records}"
        summary = Paragraph(summary_text, summary_style)
        elements.append(summary)
        elements.append(Spacer(1, 0.2*inch))
        
        # Prepare table data
        table_data = [
            ['User ID', 'Username', 'Name', 'Date', 'Time', 'Status', 'Subject', 'Session']
        ]
        
        for attendance in attendances:
            table_data.append([
                str(attendance.user.unique_id),
                str(attendance.user.username),
                f"{attendance.user.first_name} {attendance.user.last_name}",
                str(attendance.date),
                str(attendance.time.strftime('%H:%M:%S') if attendance.time else ''),
                str(attendance.status),
                str(attendance.subject or ''),
                str(attendance.session or ''),
            ])
        
        # Create table with proper column widths
        col_widths = [0.6*inch, 0.8*inch, 1.5*inch, 1.2*inch, 0.7*inch, 0.7*inch, 0.7*inch, 0.8*inch]
        table = Table(table_data, colWidths=col_widths, repeatRows=1)
        
        # Style the table
        table.setStyle(TableStyle([
            # Header styling
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a237e')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 9),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('TOPPADDING', (0, 0), (-1, 0), 12),
            
            # Data rows styling
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('ALIGN', (0, 1), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('TOPPADDING', (0, 1), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
            
            # Grid
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            
            # Alternating row colors
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f5f5f5')]),
        ]))
        
        elements.append(table)
        
        # Add footer
        elements.append(Spacer(1, 0.3*inch))
        footer_style = ParagraphStyle(
            'Footer',
            parent=styles['Normal'],
            fontSize=8,
            textColor=colors.HexColor('#757575'),
            alignment=TA_CENTER,
            fontName='Helvetica-Oblique'
        )
        footer_text = f"Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | Face Recognition Attendance System"
        footer = Paragraph(footer_text, footer_style)
        elements.append(footer)
        
        # Build PDF
        doc.build(elements)
        
        # Get PDF data
        buffer.seek(0)
        pdf_data = buffer.getvalue()
        buffer.close()
        
        # Create email
        subject = f'Attendance Report - {report_type.title()} ({start_date} to {end_date})'
        message = f"""
        Dear User,
        
        Attached is the {report_type} attendance report for the duration {start_date} to {end_date}.
        
        Total Records: {total_records}
        
        Best regards,
        Face Recognition Attendance System
        """
        
        email = EmailMessage(
            subject=subject,
            body=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[user_email],
        )
        
        # Attach PDF file
        filename = f'attendance_report_{start_date}_{end_date}.pdf'
        email.attach(filename, pdf_data, 'application/pdf')
        
        # Send email
        email.send()
        
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        import traceback
        traceback.print_exc()
        return False


def get_daily_report(date=None):
    """Get attendance records for a specific date"""
    if date is None:
        date = timezone.now().date()
    return Attendance.objects.filter(date=date).select_related('user')


def get_monthly_report(year=None, month=None):
    """Get attendance records for a specific month"""
    if year is None or month is None:
        now = timezone.now()
        year = now.year
        month = now.month
    
    return Attendance.objects.filter(
        date__year=year,
        date__month=month
    ).select_related('user')


def get_user_report(user_id, start_date=None, end_date=None):
    """Get attendance records for a specific user"""
    query = Attendance.objects.filter(user_id=user_id)
    
    if start_date:
        query = query.filter(date__gte=start_date)
    if end_date:
        query = query.filter(date__lte=end_date)
    
    return query.select_related('user')


def get_date_range_report(start_date, end_date):
    """Get attendance records for a date range"""
    return Attendance.objects.filter(
        date__gte=start_date,
        date__lte=end_date
    ).select_related('user')
