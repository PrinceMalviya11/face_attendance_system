"""
Face Recognition App Models
"""
from django.db import models
from django.conf import settings


class FaceData(models.Model):
    """
    Track face dataset collection for each user
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='face_data')
    dataset_collected = models.BooleanField(default=False)
    samples_count = models.IntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Face Data'
        verbose_name_plural = 'Face Data'
    
    def __str__(self):
        return f"Face data for {self.user.username}"
