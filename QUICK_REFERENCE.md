# Face Recognition Attendance System - Quick Reference

## 🚀 Quick Commands

### Start Server
```bash
python manage.py runserver
```
Access at: http://127.0.0.1:8000/

### Create Admin User
```bash
python manage.py createsuperuser
```

### Database Operations
```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Check for issues
python manage.py check
```

---

## 📱 Main URLs

| Page | URL | Access |
|------|-----|--------|
| Login | `/accounts/login/` | Public |
| Dashboard | `/dashboard/` | Authenticated |
| Admin Dashboard | `/dashboard/admin/` | Admin only |
| User Dashboard | `/dashboard/user/` | User only |
| User List | `/users/` | Admin only |
| Add User | `/users/create/` | Admin only |
| Mark Attendance | `/attendance/mark/` | Authenticated |
| Attendance History | `/attendance/history/` | Authenticated |
| Train Model | `/face/train/` | Admin only |
| Daily Report | `/attendance/reports/daily/` | Admin only |
| Monthly Report | `/attendance/reports/monthly/` | Admin only |

---

## 👥 Default Roles

### Admin
- Full system access
- User management
- Face data capture
- Model training
- All reports
- System configuration

### User
- Personal dashboard
- Mark own attendance
- View own attendance history
- View profile

---

## 🎯 Common Tasks

### Add a New User
1. Login as admin
2. Go to Users → Add New User
3. Fill in details (username, email, unique ID, etc.)
4. Set role (Admin/User)
5. Set password
6. Click Create User

### Capture Face Data
1. Go to Users → Select user
2. Click "Capture Face Data"
3. Allow webcam access
4. Click "Start Face Capture"
5. Wait for 20 samples to be captured
6. Verify success message

### Train Model
1. Ensure at least one user has face data
2. Go to "Train Model"
3. Click "Start Training"
4. Wait for completion
5. Verify model file created

### Mark Attendance
1. Go to "Mark Attendance"
2. Allow webcam access
3. Face the camera
4. Click "Mark Attendance"
5. Verify attendance marked

### Generate Report
1. Go to Reports menu
2. Select report type (Daily/Monthly/User)
3. Choose date/date range
4. Click "Export" for CSV/Excel
5. Or click "Send Email" for email delivery

---

## 🔑 Important Files & Directories

```
Face_Attendance_System/
├── db.sqlite3                  # Database file
├── manage.py                   # Django management script
├── requirements.txt            # Python dependencies
│
├── media/
│   └── faces/                  # Face images (user_id/face_*.jpg)
│
├── models/
│   └── face_model.yml          # Trained LBPH model
│
├── haarcascades/
│   └── haarcascade_frontalface_default.xml
│
├── static/
│   ├── css/style.css           # Custom styles
│   └── js/main.js              # JavaScript functions
│
└── templates/
    └── base.html               # Base template
```

---

## ⚙️ Configuration

### Email Settings (Optional)
Set environment variables:
```bash
# Windows CMD
set EMAIL_HOST_USER=your-email@gmail.com
set EMAIL_HOST_PASSWORD=your-app-password

# Windows PowerShell
$env:EMAIL_HOST_USER="your-email@gmail.com"
$env:EMAIL_HOST_PASSWORD="your-app-password"
```

### Face Recognition Settings
Edit `settings.py`:
```python
CONFIDENCE_THRESHOLD = 50      # Lower = stricter matching
NUM_FACE_SAMPLES = 20          # Samples per user
```

---

## 🐛 Quick Troubleshooting

### Webcam Not Working
```bash
# Check if webcam is available
python -c "import cv2; print(cv2.VideoCapture(0).isOpened())"
```
Should print: `True`

### Face Not Recognized
1. Check if user has face data: Users → View user
2. Check if model is trained: Dashboard → Model Status
3. Improve lighting
4. Face camera directly

### Import Errors
```bash
# Reinstall dependencies
pip install -r requirements.txt
```

### Database Errors
```bash
# Reset database (WARNING: Deletes all data)
del db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

---

## 📊 Model Information

### Haar Cascade
- **File**: `haarcascade_frontalface_default.xml`
- **Purpose**: Face detection
- **Parameters**: scaleFactor=1.1, minNeighbors=5

### LBPH Recognizer
- **File**: `models/face_model.yml`
- **Purpose**: Face recognition
- **Confidence**: Lower is better (threshold: 50)
- **Training**: Required after adding new users

---

## 🔒 Security Notes

- **Passwords**: Hashed with PBKDF2
- **Sessions**: 24-hour timeout
- **CSRF**: Protected on all forms
- **Permissions**: Role-based access control

---

## 📈 Performance Tips

1. **Good Lighting**: Ensure adequate lighting for face capture
2. **Multiple Angles**: Capture faces from different angles
3. **Regular Training**: Retrain model when adding multiple users
4. **Clean Database**: Remove inactive users periodically
5. **Browser**: Use Chrome for best webcam performance

---

## 🎓 For Viva/Presentation

### Key Points to Remember

**1. What is this system?**
- Web-based attendance system using face recognition
- Built with Django and OpenCV
- Automated attendance marking

**2. Technologies Used?**
- Backend: Python 3.11, Django 5.0
- Computer Vision: OpenCV, Haar Cascade, LBPH
- Frontend: HTML, CSS, JavaScript, Bootstrap 5
- Database: SQLite

**3. How does face recognition work?**
- Haar Cascade detects faces in images
- LBPH recognizes and identifies faces
- Confidence threshold validates matches

**4. Main Features?**
- User management
- Face dataset collection (20 samples)
- Model training
- Automated attendance
- Reports (CSV, Excel, Email)
- Admin and User dashboards

**5. Security Features?**
- Password hashing
- CSRF protection
- Role-based access
- Session management

---

## 📞 Quick Help

| Issue | Solution |
|-------|----------|
| Can't login | Check username/password, create superuser |
| Webcam not working | Check permissions, close other apps |
| Face not recognized | Capture face data, train model |
| Import errors | Run `pip install -r requirements.txt` |
| Server won't start | Check port 8000, run `python manage.py check` |

---

## ✅ Pre-Deployment Checklist

- [ ] All dependencies installed
- [ ] Migrations applied
- [ ] Superuser created
- [ ] Haar Cascade file present
- [ ] Webcam working
- [ ] Server starts without errors
- [ ] Can login successfully
- [ ] Can create users
- [ ] Can capture face data
- [ ] Can train model
- [ ] Can mark attendance
- [ ] Can generate reports

---

**Quick Reference Version**: 1.0  
**Last Updated**: February 2026

For detailed information, see:
- README.md - Complete user guide
- DOCUMENTATION.md - Technical details
- SETUP_GUIDE.md - Installation guide
