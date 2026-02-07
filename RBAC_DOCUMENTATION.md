# Role-Based Access Control (RBAC) System

## Overview
This Face Recognition Attendance System implements a **strict role-based access control** system with two distinct roles:

### Roles

#### 1. **ADMIN** (Superuser)
- **Creation**: Only ONE superuser can be created using `python manage.py createsuperuser`
- **Permissions**: Full system access
  - User management (Create, Read, Update, Delete)
  - Attendance management
  - Report generation and email delivery
  - System settings
  - Face dataset management
  - All admin dashboard features

#### 2. **USER** (Regular User)
- **Creation**: 
  - Public signup at `/accounts/signup/` (self-registration)
  - Created by admin through admin dashboard
- **Permissions**: Limited access
  - View own attendance records
  - Collect face dataset
  - View own profile
  - Mark attendance via face recognition
  - User dashboard access only

---

## Key Features

### ✅ 1. Public Signup Page
- **URL**: `/accounts/signup/`
- **Access**: Public (no login required)
- **Behavior**: 
  - Creates USER role accounts only
  - Automatically creates UserProfile
  - Redirects to login after successful registration
  - Link available on login page

### ✅ 2. Only ONE Superuser
- **Enforcement**: Custom `createsuperuser` management command
- **Behavior**:
  - Checks if superuser already exists
  - Prevents creation of multiple superusers
  - Shows helpful error message with existing superuser details
  - Guides admins to create additional admin users through dashboard

### ✅ 3. Superuser = Admin
- **Auto-sync**: `CustomUser.save()` method automatically syncs superuser status with ADMIN role
- **Logic**:
  ```python
  if user.is_superuser:
      user.role = 'ADMIN'
      user.is_staff = True
  ```
- **Result**: Superuser always has ADMIN role

### ✅ 4. All Other Accounts = User
- **Public Signup**: `PublicSignupForm.save()` enforces `role='USER'`
- **Default**: `CustomUser.role` defaults to 'USER' in model
- **Protection**: Public signup form doesn't expose role field

### ✅ 5. Strict Role-Based Access
- **Custom Decorators**:
  - `@admin_required`: Restricts view to ADMIN only
  - `@user_required`: Restricts view to USER only
  - `@role_required('ADMIN', 'USER')`: Flexible role checking

---

## Implementation Details

### Model: `CustomUser`
```python
class CustomUser(AbstractUser):
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='USER')
    
    def save(self, *args, **kwargs):
        if self.is_superuser:
            self.role = 'ADMIN'
            self.is_staff = True
        super().save(*args, **kwargs)
    
    def is_admin(self):
        return self.role == 'ADMIN' or self.is_superuser
    
    def is_regular_user(self):
        return self.role == 'USER'
```

### Forms

#### PublicSignupForm
- Used for public registration
- Excludes `role` field
- Overrides `save()` to force `role='USER'`

#### CustomUserCreationForm
- Used by admins to create users
- Includes `role` field for admin control
- Available only through admin dashboard

### Views Protection

#### Admin-Only Views
```python
@admin_required
def user_list(request):
    # Only accessible by ADMIN
    pass
```

#### User-Only Views
```python
@user_required
def user_dashboard(request):
    # Only accessible by USER
    pass
```

### URL Structure
```
/accounts/login/          - Public login
/accounts/signup/         - Public signup (creates USER)
/accounts/register/       - Admin-only registration (can set role)
/accounts/logout/         - Logout

/users/                   - Admin-only: User list
/users/create/            - Admin-only: Create user
/users/<id>/              - Admin-only: User detail
/users/<id>/edit/         - Admin-only: Edit user
/users/<id>/delete/       - Admin-only: Delete user

/dashboard/admin/         - Admin dashboard
/dashboard/user/          - User dashboard
```

---

## Security Measures

### 1. **Superuser Enforcement**
- Custom management command prevents multiple superusers
- Clear error messages guide proper user creation

### 2. **Role Protection**
- Public signup cannot create ADMIN users
- Role field hidden from public forms
- Server-side validation in form's `save()` method

### 3. **Access Control**
- Custom decorators enforce role-based access
- Automatic redirection for unauthorized access
- User-friendly error messages

### 4. **Auto-sync Logic**
- Superuser status automatically sets ADMIN role
- Prevents role/permission mismatches

---

## Usage Guide

### Creating the First Admin (Superuser)
```bash
python manage.py createsuperuser
```
- Enter username, email, password
- Automatically gets ADMIN role
- Full system access

### Creating Additional Users

#### Option 1: Public Signup (USER role)
1. Visit `/accounts/signup/`
2. Fill registration form
3. Account created as USER role
4. Login to access user dashboard

#### Option 2: Admin Creates User
1. Login as admin
2. Go to User Management
3. Click "Create User"
4. Fill form and select role (ADMIN or USER)
5. User created with selected role

### Attempting Second Superuser
```bash
python manage.py createsuperuser
```
**Result**:
```
❌ ERROR: A superuser already exists!
   Username: admin
   Email: admin@example.com
   Created: 2026-02-04 16:00:00

Only ONE superuser is allowed in this system.
The superuser has ADMIN role with full system access.

To create additional admin users, login as the superuser and use:
  - Admin Dashboard > User Management > Create User
  - Set role to "ADMIN" for admin privileges
```

---

## Testing Role-Based Access

### Test 1: Public Signup Creates USER
```python
# Visit /accounts/signup/
# Fill form and submit
# Check: user.role == 'USER'
```

### Test 2: Superuser Gets ADMIN Role
```bash
python manage.py createsuperuser
# Check: user.role == 'ADMIN'
# Check: user.is_superuser == True
```

### Test 3: Only One Superuser
```bash
python manage.py createsuperuser  # First time: Success
python manage.py createsuperuser  # Second time: Error
```

### Test 4: Admin-Only Access
```python
# Login as USER
# Try to access /users/
# Result: Redirected with error message
```

### Test 5: User-Only Access
```python
# Login as ADMIN
# Try to access user-specific pages
# Result: Redirected to admin dashboard
```

---

## Error Messages

### Unauthorized Access (Non-Admin)
```
🚫 Access Denied: This page is restricted to administrators only.
```

### Unauthorized Access (Non-User)
```
ℹ️ This page is for regular users. You have been redirected to the admin dashboard.
```

### Multiple Superuser Attempt
```
❌ ERROR: A superuser already exists!
[Details and instructions shown]
```

---

## Best Practices

1. **Create ONE superuser** via `createsuperuser` command
2. **Use public signup** for regular users
3. **Use admin dashboard** to create additional admin users
4. **Never modify** role manually in database
5. **Test access control** after any changes
6. **Review permissions** regularly

---

## File Structure
```
accounts/
├── models.py              # CustomUser with role logic
├── forms.py               # PublicSignupForm, CustomUserCreationForm
├── views.py               # Login, signup, register views
├── decorators.py          # admin_required, user_required
├── management/
│   └── commands/
│       └── createsuperuser.py  # Custom superuser command
└── urls.py                # URL routing

users/
├── views.py               # User management (admin-only)
└── models.py              # UserProfile

templates/
└── accounts/
    ├── login.html         # Login page with signup link
    └── signup.html        # Public signup page
```

---

## Summary

✅ **Signup page added** - Public signup at `/accounts/signup/`  
✅ **Only ONE superuser** - Enforced via custom management command  
✅ **Superuser = Admin** - Auto-sync in `CustomUser.save()`  
✅ **All other accounts = User** - Enforced in `PublicSignupForm.save()`  
✅ **Strict role-based access** - Custom decorators on all views  

**System Status**: Fully implemented and secured! 🎉
