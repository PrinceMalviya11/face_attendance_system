# Google OAuth2 Setup Checklist

Use this checklist to ensure proper setup of Google OAuth2 login.

## ✅ Pre-Setup (Already Done)

- [x] Installed django-allauth and python-decouple
- [x] Updated settings.py with OAuth2 configuration
- [x] Created custom social account adapter
- [x] Updated login page with Google button
- [x] Made unique_id field optional
- [x] Created .env file template
- [x] Run migrations
- [x] Created documentation

## 📋 Your Setup Tasks

### 1. Google Cloud Console Setup
- [ ] Go to https://console.cloud.google.com/apis/credentials
- [ ] Create new project (or select existing)
- [ ] Enable Google+ API
- [ ] Create OAuth Client ID (Web application)
- [ ] Add redirect URI: `http://localhost:8000/accounts/google/login/callback/`
- [ ] Copy Client ID
- [ ] Copy Client Secret

### 2. Environment Configuration
- [ ] Open `.env` file in project root
- [ ] Paste Client ID into `GOOGLE_OAUTH_CLIENT_ID`
- [ ] Paste Client Secret into `GOOGLE_OAUTH_CLIENT_SECRET`
- [ ] Save the file

### 3. Django Admin Configuration
- [ ] Start server: `python manage.py runserver`
- [ ] Login to admin: http://localhost:8000/admin/
- [ ] Go to **Sites** section
- [ ] Update site domain to: `localhost:8000`
- [ ] Go to **Social applications**
- [ ] Click **Add social application**
- [ ] Set Provider: **Google**
- [ ] Set Name: **Google OAuth**
- [ ] Paste Client ID
- [ ] Paste Client Secret
- [ ] Select site: `localhost:8000`
- [ ] Save

### 4. Testing
- [ ] Go to: http://localhost:8000/accounts/login/
- [ ] Verify "Continue with Google" button appears
- [ ] Click the button
- [ ] Select Google account
- [ ] Grant permissions
- [ ] Verify redirect to User Dashboard
- [ ] Check user is created with USER role
- [ ] Verify UserProfile is created
- [ ] Test face recognition with OAuth user

### 5. Verification
- [ ] OAuth users have USER role
- [ ] OAuth users cannot access admin panel
- [ ] Admin login still uses username/password
- [ ] Email is stored correctly
- [ ] unique_id is auto-generated
- [ ] UserProfile exists for OAuth user

## 🔐 Security Checklist

- [ ] `.env` file is in `.gitignore`
- [ ] Client Secret is not in code
- [ ] OAuth is disabled for admin login
- [ ] All OAuth users have USER role only
- [ ] is_staff and is_superuser are False for OAuth users

## 📚 Documentation Review

- [ ] Read OAUTH_GETTING_STARTED.md
- [ ] Review OAUTH_QUICK_REFERENCE.md
- [ ] Bookmark GOOGLE_OAUTH_SETUP.md for reference

## 🚀 Production Checklist (When Deploying)

- [ ] Update Google Console with production domain
- [ ] Add production redirect URI
- [ ] Set DEBUG = False
- [ ] Set ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
- [ ] Enable HTTPS settings
- [ ] Update Site domain in admin
- [ ] Set production environment variables
- [ ] Test OAuth flow on production

## ❌ Common Issues

If you encounter issues, check:

- [ ] Redirect URI matches exactly (no trailing slash issues)
- [ ] Site is configured in Django Admin
- [ ] Social Application is added with correct credentials
- [ ] .env file is in project root (same folder as manage.py)
- [ ] Server is running on localhost:8000
- [ ] Browser cache is cleared

## 📞 Help Resources

- **Quick Start**: OAUTH_GETTING_STARTED.md
- **Quick Reference**: OAUTH_QUICK_REFERENCE.md
- **Full Guide**: GOOGLE_OAUTH_SETUP.md
- **Technical Details**: OAUTH_IMPLEMENTATION_SUMMARY.md

---

## ✨ Status

Once all checkboxes are complete, your Google OAuth2 login is fully functional!

**Estimated Time**: 10-15 minutes

**Difficulty**: Easy (just follow the steps)

**Support**: All documentation is in the project folder
