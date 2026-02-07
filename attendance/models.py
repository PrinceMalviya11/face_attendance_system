"""
Attendance Models
Stores attendance records
"""
from django.db import models
from django.conf import settings
from django.utils import timezone


def get_current_date():
    """Get current date in configured timezone"""
    return timezone.localtime(timezone.now()).date()


def get_current_time():
    """Get current time in configured timezone"""
    return timezone.localtime(timezone.now()).time()



class Attendance(models.Model):
    """
    Attendance record for each user
    """
    STATUS_CHOICES = (
        ('PRESENT', 'Present'),
        ('ABSENT', 'Absent'),
        ('LATE', 'Late'),
    )
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='attendances')
    date = models.DateField(default=get_current_date)
    time = models.TimeField(default=get_current_time)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PRESENT')
    subject = models.CharField(max_length=100, blank=True, null=True)
    session = models.CharField(max_length=100, blank=True, null=True)
    marked_by = models.CharField(max_length=50, default='Face Recognition')
    confidence = models.FloatField(blank=True, null=True, help_text="Face recognition confidence")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Attendance'
        verbose_name_plural = 'Attendances'
        ordering = ['-date', '-time']
        unique_together = ['user', 'date', 'session']
    
    def __str__(self):
        return f"{self.user.username} - {self.date} - {self.status}"
    
    @classmethod
    def mark_attendance(cls, user, subject=None, session=None, confidence=None):
        """
        Mark attendance for a user
        Prevents duplicate attendance for the same day and session
        
        Returns:
            tuple: (attendance_object, created)
        """
        today = get_current_date()
        current_time = get_current_time()
        
        # Check if attendance already exists
        attendance, created = cls.objects.get_or_create(
            user=user,
            date=today,
            session=session or 'Default',
            defaults={
                'time': current_time,
                'status': 'PRESENT',
                'subject': subject,
                'confidence': confidence,
            }
        )
        
        return attendance, created
