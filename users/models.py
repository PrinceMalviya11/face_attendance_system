"""
User Profile Model
Stores additional user information and face dataset status
"""
from django.db import models
from django.conf import settings


class UserProfile(models.Model):
    """
    Extended user profile with face recognition data
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    profile_image = models.ImageField(upload_to='profiles/', blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    
    # Face recognition status
    face_dataset_collected = models.BooleanField(default=False)
    face_samples_count = models.IntegerField(default=0)
    last_dataset_update = models.DateTimeField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'
    
    def __str__(self):
        return f"Profile of {self.user.username}"
    
    def has_face_data(self):
        """Check if user has completed face dataset collection"""
        return self.face_dataset_collected and self.face_samples_count >= settings.NUM_FACE_SAMPLES
