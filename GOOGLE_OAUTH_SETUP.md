# Google OAuth2 Login Setup Guide

## Overview

This guide explains how to set up Google OAuth2 authentication for the Face Recognition Attendance System. OAuth2 login is **enabled for users only** - admin authentication remains unchanged using Django's default username/password login.

## Features

✅ **User-Only OAuth**: Google login is available only for regular users (students/employees)  
✅ **Admin Protection**: Admins must use username/password login  
✅ **Auto Account Creation**: New users are automatically created on first Google login  
✅ **Profile Integration**: User profiles are automatically created for OAuth users  
✅ **Face Recognition Link**: OAuth accounts can be linked with face recognition profiles  
✅ **Secure**: Uses production-ready `django-allauth` library  

---

## Step 1: Install Dependencies

First, install the required packages:

```bash
pip install -r requirements.txt
```

This will install:
- `django-allauth==0.57.0` - OAuth2 authentication
- `python-decouple==3.8` - Environment variable management

---

## Step 2: Create Google OAuth2 Credentials

### 2.1 Go to Google Cloud Console

1. Visit: https://console.cloud.google.com/
2. Sign in with your Google account
3. Create a new project or select an existing one

### 2.2 Enable Google+ API

1. Go to **APIs & Services** > **Library**
2. Search for "Google+ API"
3. Click **Enable**

### 2.3 Create OAuth2 Credentials

1. Go to **APIs & Services** > **Credentials**
2. Click **Create Credentials** > **OAuth client ID**
3. If prompted, configure the OAuth consent screen:
   - **User Type**: External
   - **App Name**: Face Recognition Attendance System
   - **User support email**: Your email
   - **Developer contact**: Your email
   - **Scopes**: Add `email` and `profile`
   - **Test users**: Add your email for testing

4. Create OAuth Client ID:
   - **Application type**: Web application
   - **Name**: Face Attendance OAuth
   - **Authorized JavaScript origins**:
     ```
     http://localhost:8000
     http://127.0.0.1:8000
     ```
   - **Authorized redirect URIs**:
     ```
     http://localhost:8000/accounts/google/login/callback/
     http://127.0.0.1:8000/accounts/google/login/callback/
     ```

5. Click **Create**
6. Copy the **Client ID** and **Client Secret**

### 2.4 For Production (Optional)

When deploying to production, add your production domain:

**Authorized JavaScript origins**:
```
https://yourdomain.com
```

**Authorized redirect URIs**:
```
https://yourdomain.com/accounts/google/login/callback/
```

---

## Step 3: Configure Environment Variables

### 3.1 Create .env file

Create a `.env` file in the project root (same directory as `manage.py`):

```bash
# Copy from example
copy .env.example .env
```

### 3.2 Add Google OAuth Credentials

Edit the `.env` file and add your credentials:

```env
# Google OAuth2 Configuration
GOOGLE_OAUTH_CLIENT_ID=your-client-id-here.apps.googleusercontent.com
GOOGLE_OAUTH_CLIENT_SECRET=your-client-secret-here

# Email Configuration (existing)
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Django Secret Key (optional - for production)
SECRET_KEY=your-secret-key-here
```

**Important**: Replace `your-client-id-here` and `your-client-secret-here` with the actual values from Google Cloud Console.

---

## Step 4: Run Database Migrations

The OAuth2 setup requires new database tables:

```bash
python manage.py makemigrations
python manage.py migrate
```

This will create tables for:
- `django.contrib.sites`
- `allauth.account`
- `allauth.socialaccount`
- Updated `CustomUser` model (unique_id is now optional)

---

## Step 5: Configure Site Domain

### 5.1 Access Django Admin

1. Start the development server:
   ```bash
   python manage.py runserver
   ```

2. Go to: http://localhost:8000/admin/
3. Login with your admin credentials

### 5.2 Update Site Configuration

1. Navigate to **Sites** section
2. Click on **example.com**
3. Update:
   - **Domain name**: `localhost:8000` (or `127.0.0.1:8000`)
   - **Display name**: `Face Attendance System`
4. Click **Save**

### 5.3 Add Google Social Application

1. Navigate to **Social applications**
2. Click **Add social application**
3. Fill in:
   - **Provider**: Google
   - **Name**: Google OAuth
   - **Client id**: Your Google Client ID
   - **Secret key**: Your Google Client Secret
   - **Sites**: Select `localhost:8000` and move it to "Chosen sites"
4. Click **Save**

---

## Step 6: Test Google OAuth Login

### 6.1 Test User Login

1. Go to: http://localhost:8000/accounts/login/
2. You should see:
   - Traditional login form (username/password)
   - **OR** divider
   - **Continue with Google** button

3. Click **Continue with Google**
4. Select your Google account
5. Grant permissions
6. You should be redirected to the User Dashboard

### 6.2 Verify User Creation

1. Login to Django Admin: http://localhost:8000/admin/
2. Go to **Users**
3. You should see the new user created via Google OAuth:
   - **Role**: USER
   - **Email**: From Google account
   - **Username**: Auto-generated
   - **unique_id**: Auto-generated

### 6.3 Test Admin Login (Should NOT use OAuth)

1. Logout
2. Go to: http://localhost:8000/admin/
3. Admin login should use traditional username/password
4. OAuth should NOT be available on admin login page

---

## How It Works

### User Authentication Flow

1. **User clicks "Continue with Google"**
   - Redirects to Google OAuth consent screen
   - User grants permissions

2. **Google redirects back with user data**
   - Email, name, profile picture

3. **Custom adapter processes the data**
   - Checks if user with email exists
   - If exists: Links OAuth account to existing user
   - If new: Creates new user with USER role

4. **User profile is created**
   - Automatically creates `UserProfile` instance
   - Generates unique `unique_id`

5. **User is logged in**
   - Redirects to User Dashboard
   - Can now mark attendance via face recognition

### Admin Protection

- **Admin login**: Uses Django's default authentication (username/password)
- **OAuth users**: Cannot access admin panel (role=USER, is_staff=False)
- **Separation**: Admin and user authentication flows are completely separate

### Face Recognition Integration

OAuth users can use face recognition for attendance:

1. **After OAuth login**: User is logged in with USER role
2. **Register face**: User can register their face via the dashboard
3. **Mark attendance**: Face recognition system links to the OAuth user account
4. **Reports**: Attendance records are mapped to the authenticated user

---

## Security Best Practices

### 1. Environment Variables

✅ **DO**: Store credentials in `.env` file  
❌ **DON'T**: Commit `.env` to Git (already in `.gitignore`)

### 2. HTTPS in Production

Update `settings.py` for production:

```python
# Production settings
DEBUG = False
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True
```

### 3. Email Verification

For production, enable mandatory email verification:

```python
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
```

### 4. OAuth Scope

Only request necessary scopes:
- `profile` - Name, profile picture
- `email` - Email address

### 5. Client Secret Protection

- Never expose Client Secret in frontend code
- Store in environment variables only
- Rotate secrets if compromised

---

## Troubleshooting

### Issue 1: "Redirect URI mismatch"

**Error**: The redirect URI in the request does not match

**Solution**:
1. Check Google Cloud Console > Credentials
2. Ensure redirect URI is exactly: `http://localhost:8000/accounts/google/login/callback/`
3. No trailing spaces or extra characters

### Issue 2: "Site matching query does not exist"

**Error**: Site matching query does not exist

**Solution**:
1. Run migrations: `python manage.py migrate`
2. Update Site in Django Admin (see Step 5.2)

### Issue 3: "Social application not found"

**Error**: Social application for Google not found

**Solution**:
1. Add Social Application in Django Admin (see Step 5.3)
2. Ensure Client ID and Secret are correct
3. Ensure Site is selected in "Chosen sites"

### Issue 4: OAuth user cannot login

**Error**: User created but cannot login

**Solution**:
1. Check user role: Should be "USER"
2. Check `is_active`: Should be True
3. Check UserProfile: Should be created automatically

### Issue 5: Admin can use OAuth (should not)

**Error**: Admin can login via Google

**Solution**:
1. OAuth is for users only
2. Admins should use: http://localhost:8000/admin/
3. Regular login page is for both, but OAuth creates USER role only

---

## Configuration Files

### Files Modified

1. **requirements.txt** - Added django-allauth, python-decouple
2. **settings.py** - OAuth2 configuration
3. **urls.py** - Added allauth URLs
4. **accounts/models.py** - Made unique_id optional
5. **accounts/adapters.py** - Custom OAuth adapter (NEW)
6. **templates/accounts/login.html** - Added Google button
7. **.env.example** - Added OAuth credentials template

### New Database Tables

- `django_site`
- `account_emailaddress`
- `account_emailconfirmation`
- `socialaccount_socialaccount`
- `socialaccount_socialapp`
- `socialaccount_socialapp_sites`
- `socialaccount_socialtoken`

---

## Testing Checklist

- [ ] Google OAuth button appears on login page
- [ ] Clicking button redirects to Google consent screen
- [ ] After authentication, user is created with USER role
- [ ] UserProfile is created automatically
- [ ] User is redirected to User Dashboard
- [ ] User can mark attendance via face recognition
- [ ] Admin login still uses username/password
- [ ] OAuth users cannot access admin panel
- [ ] Email is stored correctly
- [ ] unique_id is auto-generated

---

## Production Deployment

### 1. Update Google Cloud Console

Add production domain to:
- Authorized JavaScript origins
- Authorized redirect URIs

### 2. Update Django Settings

```python
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com']
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
```

### 3. Update Site Configuration

In Django Admin:
- Domain: `yourdomain.com`
- Display name: Your app name

### 4. Environment Variables

Set production environment variables:
```env
SECRET_KEY=production-secret-key
GOOGLE_OAUTH_CLIENT_ID=production-client-id
GOOGLE_OAUTH_CLIENT_SECRET=production-client-secret
```

---

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review Google Cloud Console configuration
3. Check Django logs: `python manage.py runserver` output
4. Verify environment variables are loaded correctly

---

## Summary

✅ Google OAuth2 is now configured for user login  
✅ Admin authentication remains unchanged  
✅ Users can login with Google and use face recognition  
✅ Secure, production-ready implementation  
✅ Clean separation between admin and user flows  

**Next Steps**:
1. Get Google OAuth credentials
2. Update `.env` file
3. Run migrations
4. Configure Site and Social Application in admin
5. Test the login flow
