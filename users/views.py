"""
User Management Views
Admin CRUD operations for user management
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from accounts.models import CustomUser
from accounts.forms import CustomUserCreationForm, UserUpdateForm
from accounts.decorators import admin_required
from .models import UserProfile


@admin_required
def user_list(request):
    """
    Display list of all users (Admin only)
    """
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        users = CustomUser.objects.filter(
            Q(username__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(unique_id__icontains=search_query) |
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query)
        ).order_by('-created_at')
    else:
        users = CustomUser.objects.all().order_by('-created_at')
    
    context = {
        'users': users,
        'search_query': search_query,
    }
    return render(request, 'users/user_list.html', context)


@admin_required
def user_detail(request, user_id):
    """
    Display detailed information about a specific user
    """
    
    user = get_object_or_404(CustomUser, id=user_id)
    profile, created = UserProfile.objects.get_or_create(user=user)
    
    context = {
        'user_obj': user,
        'profile': profile,
    }
    return render(request, 'users/user_detail.html', context)


@admin_required
def user_create(request):
    """
    Create a new user (Admin only)
    """
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create user profile
            UserProfile.objects.create(user=user)
            messages.success(request, f'User {user.username} created successfully!')
            return redirect('users:user_detail', user_id=user.id)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'users/user_form.html', {'form': form, 'action': 'Create'})


@admin_required
def user_update(request, user_id):
    """
    Update user information (Admin only)
    """
    
    user = get_object_or_404(CustomUser, id=user_id)
    
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, f'User {user.username} updated successfully!')
            return redirect('users:user_detail', user_id=user.id)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserUpdateForm(instance=user)
    
    return render(request, 'users/user_form.html', {'form': form, 'action': 'Update', 'user_obj': user})


@admin_required
def user_delete(request, user_id):
    """
    Delete a user (Admin only)
    """
    
    user = get_object_or_404(CustomUser, id=user_id)
    
    if request.method == 'POST':
        username = user.username
        user.delete()
        messages.success(request, f'User {username} deleted successfully!')
        return redirect('users:user_list')
    
    return render(request, 'users/user_confirm_delete.html', {'user_obj': user})
