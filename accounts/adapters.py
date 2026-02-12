"""
Custom Social Account Adapter for Google OAuth2
Ensures OAuth users are created as regular users (USER role) only
Prevents OAuth users from accessing admin panel
"""
from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.exceptions import ImmediateHttpResponse
from django.shortcuts import redirect
from django.contrib import messages
from users.models import UserProfile
import random
import string


class CustomAccountAdapter(DefaultAccountAdapter):
    """
    Custom account adapter to allow seamless OAuth signup
    """
    
    def is_open_for_signup(self, request):
        """
        Always allow signup for OAuth users
        """
        return True


class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    """
    Custom adapter to control OAuth user creation and authentication
    """
    
    def pre_social_login(self, request, sociallogin):
        """
        Invoked just after a user successfully authenticates via a social provider,
        but before the login is actually processed
        """
        # If user is already logged in, do nothing
        if request.user.is_authenticated:
            return
        
        # Check if this social account is already connected to a user
        if sociallogin.is_existing:
            return
        
        # Try to connect to existing user with same email
        try:
            email = sociallogin.account.extra_data.get('email', '').lower()
            if email:
                from accounts.models import CustomUser
                existing_user = CustomUser.objects.filter(email=email).first()
                if existing_user:
                    # Connect this social account to existing user
                    sociallogin.connect(request, existing_user)
        except Exception as e:
            pass
    
    def save_user(self, request, sociallogin, form=None):
        """
        Saves a newly signed up social login user
        Ensures user is created with USER role only
        """
        user = super().save_user(request, sociallogin, form)
        
        # Force USER role for all OAuth signups
        user.role = 'USER'
        user.is_staff = False
        user.is_superuser = False
        
        # Extract data from Google
        extra_data = sociallogin.account.extra_data
        
        # Set user fields from Google data
        if not user.first_name and extra_data.get('given_name'):
            user.first_name = extra_data.get('given_name', '')
        
        if not user.last_name and extra_data.get('family_name'):
            user.last_name = extra_data.get('family_name', '')
        
        # Generate unique_id if not set (required field)
        if not user.unique_id:
            # Generate a unique ID based on email or random string
            email_prefix = user.email.split('@')[0] if user.email else 'user'
            random_suffix = ''.join(random.choices(string.digits, k=6))
            user.unique_id = f"{email_prefix}_{random_suffix}"
            
            # Ensure uniqueness
            from accounts.models import CustomUser
            while CustomUser.objects.filter(unique_id=user.unique_id).exists():
                random_suffix = ''.join(random.choices(string.digits, k=6))
                user.unique_id = f"{email_prefix}_{random_suffix}"
        
        # Generate username if not set
        if not user.username:
            user.username = user.unique_id
        
        user.save()
        
        # Create UserProfile automatically
        try:
            UserProfile.objects.get_or_create(user=user)
        except Exception as e:
            pass
        
        return user
    
    def is_auto_signup_allowed(self, request, sociallogin):
        """
        Allow auto signup for all OAuth users
        """
        return True
    
    def populate_user(self, request, sociallogin, data):
        """
        Populate user instance with data from social provider
        """
        user = super().populate_user(request, sociallogin, data)
        
        # Ensure email is set
        if not user.email and data.get('email'):
            user.email = data.get('email')
        
        # Auto-generate username from email to prevent signup form
        if not user.username:
            email = data.get('email', '')
            if email:
                username_base = email.split('@')[0]
                user.username = username_base
                
                # Ensure username uniqueness
                from accounts.models import CustomUser
                counter = 1
                while CustomUser.objects.filter(username=user.username).exists():
                    user.username = f"{username_base}{counter}"
                    counter += 1
        
        return user
    
    def is_open_for_signup(self, request, sociallogin):
        """
        Force signup to be open for OAuth users
        """
        return True
    
    def authentication_error(self, request, provider_id, error=None, exception=None, extra_context=None):
        """
        Handle authentication errors gracefully
        """
        messages.error(request, f'Authentication failed. Please try again or use regular login.')
        raise ImmediateHttpResponse(redirect('accounts:login'))
    
    def get_signup_redirect_url(self, request):
        """
        Redirect OAuth users directly to user dashboard after signup
        """
        return '/dashboard/user/'
    
    def get_login_redirect_url(self, request):
        """
        Redirect OAuth users directly to user dashboard after login
        """
        return '/dashboard/user/'

