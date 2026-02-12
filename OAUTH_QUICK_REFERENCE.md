# Google OAuth2 - Quick Reference

## Quick Setup (5 Minutes)

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Get Google Credentials
1. Go to: https://console.cloud.google.com/apis/credentials
2. Create OAuth Client ID (Web application)
3. Add redirect URI: `http://localhost:8000/accounts/google/login/callback/`
4. Copy Client ID and Client Secret

### 3. Configure Environment
Create `.env` file:
```env
GOOGLE_OAUTH_CLIENT_ID=your-client-id.apps.googleusercontent.com
GOOGLE_OAUTH_CLIENT_SECRET=your-client-secret
```

### 4. Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Configure Django Admin
```bash
python manage.py runserver
```

1. Go to: http://localhost:8000/admin/
2. **Sites** → Update to `localhost:8000`
3. **Social applications** → Add Google OAuth app
   - Provider: Google
   - Client ID: (from step 2)
   - Secret: (from step 2)
   - Sites: Select `localhost:8000`

### 6. Test
Go to: http://localhost:8000/accounts/login/
Click "Continue with Google"

---

## Key Features

| Feature | Status |
|---------|--------|
| User OAuth Login | ✅ Enabled |
| Admin OAuth Login | ❌ Disabled (username/password only) |
| Auto User Creation | ✅ Enabled |
| Profile Auto-Creation | ✅ Enabled |
| Face Recognition Link | ✅ Supported |
| Email Verification | ⚠️ Optional (set to mandatory in production) |

---

## Important URLs

- **User Login**: http://localhost:8000/accounts/login/
- **Admin Login**: http://localhost:8000/admin/
- **OAuth Callback**: http://localhost:8000/accounts/google/login/callback/
- **Google Console**: https://console.cloud.google.com/

---

## File Changes

| File | Change |
|------|--------|
| `requirements.txt` | Added django-allauth, python-decouple |
| `settings.py` | OAuth2 configuration |
| `urls.py` | Added allauth URLs |
| `accounts/models.py` | Made unique_id optional |
| `accounts/adapters.py` | Custom OAuth adapter (NEW) |
| `templates/accounts/login.html` | Added Google button |
| `.env.example` | OAuth credentials template |

---

## Security Checklist

- [ ] `.env` file is in `.gitignore`
- [ ] Client Secret is not in code
- [ ] HTTPS enabled in production
- [ ] Email verification enabled in production
- [ ] Admin login uses username/password only
- [ ] OAuth users have USER role only

---

## Common Issues

### "Redirect URI mismatch"
→ Check Google Console redirect URI matches exactly

### "Site matching query does not exist"
→ Run migrations and update Site in admin

### "Social application not found"
→ Add Social Application in Django Admin

---

## Production Checklist

- [ ] Update Google Console with production domain
- [ ] Set `DEBUG = False`
- [ ] Set `ACCOUNT_EMAIL_VERIFICATION = 'mandatory'`
- [ ] Enable HTTPS settings
- [ ] Update Site domain in admin
- [ ] Set production environment variables

---

## Testing Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser (if needed)
python manage.py createsuperuser

# Run server
python manage.py runserver

# Test OAuth
# Go to: http://localhost:8000/accounts/login/
# Click "Continue with Google"
```

---

## Support

📖 **Full Guide**: See `GOOGLE_OAUTH_SETUP.md`  
🔧 **Troubleshooting**: Check the full guide for detailed solutions  
🌐 **Google Docs**: https://django-allauth.readthedocs.io/
