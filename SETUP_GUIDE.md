# Face Recognition Attendance System - Setup Guide

## Quick Start Guide

Follow these steps to get the system up and running:

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- Django 5.0.1
- OpenCV 4.9.0
- NumPy 1.26.3
- Pillow 10.2.0
- openpyxl 3.1.2
- xlwt 1.3.0

### Step 2: Run Database Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

This creates all necessary database tables.

### Step 3: Create Superuser (Admin Account)

```bash
python manage.py createsuperuser
```

Enter the following information when prompted:
- **Username**: admin (or your preferred username)
- **Email**: admin@example.com (or your email)
- **Password**: (choose a strong password)
- **Password (again)**: (confirm password)

### Step 4: Run the Development Server

```bash
python manage.py runserver
```

The server will start at: `http://127.0.0.1:8000/`

### Step 5: Access the Application

1. Open your web browser
2. Navigate to: `http://127.0.0.1:8000/`
3. Login with your admin credentials

---

## Initial Configuration

### 1. Configure Email Settings (Optional)

To enable email report delivery, set environment variables:

**Windows (Command Prompt):**
```cmd
set EMAIL_HOST_USER=your-email@gmail.com
set EMAIL_HOST_PASSWORD=your-app-password
```

**Windows (PowerShell):**
```powershell
$env:EMAIL_HOST_USER="your-email@gmail.com"
$env:EMAIL_HOST_PASSWORD="your-app-password"
```

**Linux/Mac:**
```bash
export EMAIL_HOST_USER=your-email@gmail.com
export EMAIL_HOST_PASSWORD=your-app-password
```

**Note**: For Gmail, you need to create an "App Password":
1. Go to Google Account Settings
2. Security → 2-Step Verification → App Passwords
3. Generate a new app password
4. Use this password in EMAIL_HOST_PASSWORD

### 2. Verify Webcam Access

Ensure your webcam is:
- Connected and working
- Not being used by another application
- Allowed in browser permissions

---

## First-Time Usage Workflow

### For Administrators:

#### 1. Login
- Navigate to `http://127.0.0.1:8000/`
- Enter admin credentials

#### 2. Add a New User
- Click **Users** → **Add New User**
- Fill in user details:
  - Username (required)
  - Email (required)
  - Unique ID / Roll No (required)
  - First Name, Last Name
  - Department
  - Role (Admin or User)
  - Password
- Click **Create User**

#### 3. Capture Face Data
- Go to **Users** → Select the user
- Click **Capture Face Data**
- Allow webcam access when prompted
- Click **Start Face Capture**
- System will automatically capture 20 face samples
- Wait for completion message

#### 4. Train the Model
- Go to **Train Model** from navigation
- Click **Start Training**
- Wait for training to complete (10-30 seconds)
- Success message will appear

#### 5. Mark Attendance
- Go to **Mark Attendance**
- Allow webcam access
- Face the camera
- Click **Mark Attendance**
- System will recognize face and mark attendance

---

## Testing the System

### Test Scenario 1: User Registration and Face Capture

1. Create a test user:
   - Username: `testuser`
   - Unique ID: `TEST001`
   - Email: `test@example.com`
   - Role: User

2. Capture face data for the test user

3. Verify face data is collected:
   - Go to Users list
   - Check "Face Data" column shows "Yes"

### Test Scenario 2: Model Training

1. Ensure at least one user has face data
2. Go to Train Model
3. Click Start Training
4. Verify success message
5. Check that `models/face_model.yml` file exists

### Test Scenario 3: Attendance Marking

1. Ensure model is trained
2. Go to Mark Attendance
3. Face the camera
4. Click Mark Attendance
5. Verify attendance is marked
6. Check Attendance History

---

## Troubleshooting Common Issues

### Issue 1: Webcam Not Working

**Symptoms**: "Failed to open webcam" error

**Solutions**:
1. Check if webcam is connected
2. Close other applications using webcam
3. Try different browser (Chrome recommended)
4. Check browser permissions for camera access
5. Restart browser

### Issue 2: Face Not Recognized

**Symptoms**: "Face not recognized" message

**Solutions**:
1. Ensure face data is collected for the user
2. Verify model is trained
3. Improve lighting conditions
4. Face camera directly
5. Remove glasses
6. Retrain model if needed

### Issue 3: Model Training Fails

**Symptoms**: "No face data found" error

**Solutions**:
1. Ensure at least one user has face data collected
2. Check `media/faces/` directory for face images
3. Verify face capture completed successfully
4. Try capturing face data again

### Issue 4: Import Errors

**Symptoms**: "ModuleNotFoundError" errors

**Solutions**:
1. Ensure virtual environment is activated
2. Run `pip install -r requirements.txt` again
3. Check Python version (3.11 required)
4. Verify all dependencies installed

### Issue 5: Database Errors

**Symptoms**: "no such table" errors

**Solutions**:
1. Run migrations: `python manage.py migrate`
2. Delete `db.sqlite3` and run migrations again
3. Check for migration files in each app

---

## Directory Structure Verification

After setup, verify these directories exist:

```
Face_Attendance_System/
├── media/
│   └── faces/          # Face images stored here
├── models/             # Trained model stored here
├── haarcascades/       # Haar Cascade classifier
├── static/             # CSS, JS files
├── templates/          # HTML templates
└── db.sqlite3          # Database file (created after migrations)
```

---

## Default Admin Credentials

After creating superuser, use these credentials to login:
- **URL**: http://127.0.0.1:8000/
- **Username**: (what you entered during createsuperuser)
- **Password**: (what you entered during createsuperuser)

---

## Next Steps

1. ✅ Complete initial setup
2. ✅ Create admin account
3. ✅ Add users
4. ✅ Capture face data
5. ✅ Train model
6. ✅ Test attendance marking
7. ✅ Generate reports
8. ✅ Configure email (optional)

---

## Support

For issues or questions:
1. Check DOCUMENTATION.md for technical details
2. Review README.md for usage guide
3. Check troubleshooting section above

---

## Production Deployment Notes

**Important**: This setup is for development only.

For production deployment:
1. Set `DEBUG = False` in settings.py
2. Configure proper SECRET_KEY
3. Use PostgreSQL/MySQL instead of SQLite
4. Set up proper web server (Nginx + Gunicorn)
5. Enable HTTPS
6. Configure static file serving
7. Set up backup system
8. Implement monitoring

---

**Setup Version**: 1.0  
**Last Updated**: February 2026
