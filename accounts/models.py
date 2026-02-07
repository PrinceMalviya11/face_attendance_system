"""
Custom User Model for Face Recognition Attendance System
Extends Django's AbstractUser to add role-based access control
"""
from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """
    Custom User model with role-based access control
    Roles: ADMIN, USER
    """
    ROLE_CHOICES = (
        ('ADMIN', 'Admin'),
        ('USER', 'User'),
    )
    
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='USER')
    unique_id = models.CharField(max_length=50, unique=True, help_text="Roll No / Employee ID")
    phone = models.CharField(max_length=15, blank=True, null=True)
    department = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.username} ({self.unique_id})"
    
    def save(self, *args, **kwargs):
        """
        Override save to ensure superuser status syncs with ADMIN role
        - If is_superuser=True, set role='ADMIN'
        - If is_superuser=False and role='ADMIN', keep role='ADMIN' (admin created by admin)
        """
        if self.is_superuser:
            self.role = 'ADMIN'
            self.is_staff = True
        super().save(*args, **kwargs)
    
    def is_admin(self):
        """Check if user has admin role or is superuser"""
        return self.role == 'ADMIN' or self.is_superuser
    
    def is_regular_user(self):
        """Check if user has regular user role"""
        return self.role == 'USER'

