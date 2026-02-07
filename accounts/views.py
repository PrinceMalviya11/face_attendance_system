"""
Authentication Views for Face Recognition Attendance System
Handles login, logout, and user registration
"""
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.csrf import csrf_protect
from .forms import CustomAuthenticationForm, CustomUserCreationForm, PublicSignupForm
from .decorators import admin_required
from users.models import UserProfile


@csrf_protect
def login_view(request):
    """
    Handle user login with role-based redirection
    Admin users -> Admin Dashboard
    Regular users -> User Dashboard
    """
    if request.user.is_authenticated:
        return redirect('dashboard:index')
    
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.first_name or user.username}!')
                
                # Role-based redirection
                if user.is_admin():
                    return redirect('dashboard:admin_dashboard')
                else:
                    return redirect('dashboard:user_dashboard')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = CustomAuthenticationForm()
    
    return render(request, 'accounts/login.html', {'form': form})


@login_required
def logout_view(request):
    """Handle user logout"""
    logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return redirect('accounts:login')


@admin_required
def register_view(request):
    """
    Admin-only user registration
    Only admins can create new users
    """
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'User {user.username} created successfully!')
            return redirect('users:user_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'accounts/register.html', {'form': form})


@csrf_protect
def signup_view(request):
    """
    Public signup view - Creates USER role accounts only
    Anyone can sign up, but all accounts are created as USER role
    """
    if request.user.is_authenticated:
        return redirect('dashboard:index')
    
    if request.method == 'POST':
        form = PublicSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create user profile automatically
            UserProfile.objects.create(user=user)
            messages.success(request, f'Account created successfully! Please login to continue.')
            return redirect('accounts:login')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = PublicSignupForm()
    
    return render(request, 'accounts/signup.html', {'form': form})

