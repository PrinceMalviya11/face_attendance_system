"""
Custom Decorators for Role-Based Access Control
Provides strict enforcement of ADMIN and USER permissions
"""
from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def admin_required(view_func):
    """
    Decorator to restrict access to ADMIN users only
    Redirects non-admin users to their dashboard with error message
    """
    @wraps(view_func)
    @login_required
    def wrapper(request, *args, **kwargs):
        if not request.user.is_admin():
            messages.error(
                request, 
                '🚫 Access Denied: This page is restricted to administrators only.'
            )
            return redirect('dashboard:user_dashboard')
        return view_func(request, *args, **kwargs)
    return wrapper


def user_required(view_func):
    """
    Decorator to restrict access to regular USER role only
    Redirects admin users to their dashboard
    """
    @wraps(view_func)
    @login_required
    def wrapper(request, *args, **kwargs):
        if not request.user.is_regular_user():
            messages.info(
                request, 
                'ℹ️ This page is for regular users. You have been redirected to the admin dashboard.'
            )
            return redirect('dashboard:admin_dashboard')
        return view_func(request, *args, **kwargs)
    return wrapper


def role_required(*allowed_roles):
    """
    Decorator to restrict access to specific roles
    Usage: @role_required('ADMIN', 'USER')
    """
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def wrapper(request, *args, **kwargs):
            if request.user.role not in allowed_roles:
                messages.error(
                    request,
                    f'🚫 Access Denied: Your role ({request.user.role}) does not have permission to access this page.'
                )
                return redirect('dashboard:index')
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator
