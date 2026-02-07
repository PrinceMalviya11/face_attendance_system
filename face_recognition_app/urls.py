"""
URL Configuration for Face Recognition App
"""
from django.urls import path
from . import views

app_name = 'face_recognition_app'

urlpatterns = [
    path('capture/<int:user_id>/', views.capture_face_view, name='capture_face'),
    path('train/', views.train_model_view, name='train_model'),
    path('video-feed/', views.video_feed, name='video_feed'),
    path('recognize-ajax/', views.recognize_face_ajax, name='recognize_ajax'),
]
