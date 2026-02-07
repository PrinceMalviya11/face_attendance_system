"""
Test Script for Role-Based Access Control System
Run this to verify all RBAC features are working correctly
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Face_Attendance_System.settings')
django.setup()

from accounts.models import CustomUser
from users.models import UserProfile
from django.contrib.auth import get_user_model

User = get_user_model()

def test_rbac_system():
    """Test all RBAC features"""
    print("\n" + "="*60)
    print("ROLE-BASED ACCESS CONTROL SYSTEM - TEST SUITE")
    print("="*60 + "\n")
    
    # Test 1: Check superuser count
    print("Test 1: Checking superuser count...")
    superusers = User.objects.filter(is_superuser=True)
    print(f"   Superusers found: {superusers.count()}")
    if superusers.count() == 0:
        print("   ✅ No superuser exists yet (create one with 'python manage.py createsuperuser')")
    elif superusers.count() == 1:
        su = superusers.first()
        print(f"   ✅ ONE superuser exists: {su.username}")
        print(f"      Role: {su.role}")
        print(f"      Is Admin: {su.is_admin()}")
    else:
        print(f"   ❌ WARNING: {superusers.count()} superusers found! Only ONE should exist.")
    
    # Test 2: Check role distribution
    print("\nTest 2: Checking role distribution...")
    admin_count = User.objects.filter(role='ADMIN').count()
    user_count = User.objects.filter(role='USER').count()
    print(f"   ADMIN users: {admin_count}")
    print(f"   USER users: {user_count}")
    print(f"   Total users: {User.objects.count()}")
    
    # Test 3: Verify superuser has ADMIN role
    print("\nTest 3: Verifying superuser has ADMIN role...")
    for su in superusers:
        if su.role == 'ADMIN':
            print(f"   ✅ Superuser '{su.username}' has ADMIN role")
        else:
            print(f"   ❌ WARNING: Superuser '{su.username}' has role '{su.role}' (should be ADMIN)")
    
    # Test 4: Check if all users have profiles
    print("\nTest 4: Checking user profiles...")
    users_without_profile = []
    for user in User.objects.all():
        try:
            profile = user.profile
        except UserProfile.DoesNotExist:
            users_without_profile.append(user.username)
    
    if users_without_profile:
        print(f"   ⚠️ Users without profile: {', '.join(users_without_profile)}")
    else:
        print(f"   ✅ All {User.objects.count()} users have profiles")
    
    # Test 5: List all users with their roles
    print("\nTest 5: User list with roles...")
    if User.objects.count() > 0:
        print("   " + "-"*56)
        print(f"   {'Username':<20} {'Role':<10} {'Superuser':<12} {'Active':<8}")
        print("   " + "-"*56)
        for user in User.objects.all()[:10]:  # Show first 10
            print(f"   {user.username:<20} {user.role:<10} {str(user.is_superuser):<12} {str(user.is_active):<8}")
        if User.objects.count() > 10:
            print(f"   ... and {User.objects.count() - 10} more users")
    else:
        print("   No users found in database")
    
    # Test 6: Check URL patterns
    print("\nTest 6: Checking URL patterns...")
    try:
        from django.urls import reverse
        urls_to_check = [
            ('accounts:login', 'Login'),
            ('accounts:signup', 'Public Signup'),
            ('accounts:register', 'Admin Register'),
            ('dashboard:index', 'Dashboard Index'),
            ('dashboard:admin_dashboard', 'Admin Dashboard'),
            ('dashboard:user_dashboard', 'User Dashboard'),
        ]
        for url_name, description in urls_to_check:
            try:
                url = reverse(url_name)
                print(f"   ✅ {description:<20} -> {url}")
            except Exception as e:
                print(f"   ❌ {description:<20} -> ERROR: {e}")
    except Exception as e:
        print(f"   ❌ Error checking URLs: {e}")
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    print("\n✅ RBAC System Status:")
    print(f"   - Superusers: {superusers.count()} (should be 0 or 1)")
    print(f"   - ADMIN users: {admin_count}")
    print(f"   - USER users: {user_count}")
    print(f"   - Total users: {User.objects.count()}")
    print(f"   - Users with profiles: {User.objects.count() - len(users_without_profile)}")
    
    print("\n📋 Next Steps:")
    if superusers.count() == 0:
        print("   1. Create superuser: python manage.py createsuperuser")
        print("   2. Run server: python manage.py runserver")
        print("   3. Login as superuser at: http://localhost:8000/accounts/login/")
        print("   4. Test public signup at: http://localhost:8000/accounts/signup/")
    else:
        print("   1. Test login at: http://localhost:8000/accounts/login/")
        print("   2. Test public signup at: http://localhost:8000/accounts/signup/")
        print("   3. Test admin dashboard access control")
        print("   4. Test user dashboard access control")
    
    print("\n" + "="*60 + "\n")

if __name__ == '__main__':
    test_rbac_system()
