"""
URL Configuration for Users App
"""
from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('', views.user_list, name='user_list'),
    path('<int:user_id>/', views.user_detail, name='user_detail'),
    path('create/', views.user_create, name='user_create'),
    path('<int:user_id>/update/', views.user_update, name='user_update'),
    path('<int:user_id>/delete/', views.user_delete, name='user_delete'),
]
