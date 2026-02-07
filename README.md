# Face Recognition Attendance System

A production-ready, web-based Face Recognition Attendance System built with Django and OpenCV. This system automatically marks attendance using live webcam feed and facial recognition technology.

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Django](https://img.shields.io/badge/Django-5.0-green)
![OpenCV](https://img.shields.io/badge/OpenCV-4.9-red)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-purple)

## 🎯 Features

### Core Functionality
- ✅ **Face Recognition**: High-accuracy face detection and recognition using Haar Cascade and LBPH algorithms
- ✅ **Automated Attendance**: Real-time attendance marking with duplicate prevention
- ✅ **Role-Based Access**: Separate Admin and User dashboards with appropriate permissions
- ✅ **User Management**: Complete CRUD operations for user management
- ✅ **Face Dataset Collection**: Capture 20 face samples per user with webcam
- ✅ **Model Training**: Train LBPH face recognizer with collected datasets
- ✅ **Attendance Reports**: Daily, monthly, and user-wise reports
- ✅ **Export Functionality**: Export reports in CSV and Excel formats
- ✅ **Email Reports**: Automatically send attendance reports via email

### Security Features
- 🔐 Secure password hashing (PBKDF2)
- 🔐 CSRF protection
- 🔐 Session-based authentication
- 🔐 Role-based access control
- 🔐 Input validation and sanitization

## 🛠️ Technology Stack

### Backend
- **Python 3.11**
- **Django 5.0** - Web framework
- **OpenCV 4.9** - Computer vision library
- **NumPy** - Numerical computing
- **Pillow** - Image processing

### Frontend
- **HTML5**
- **CSS3** - Custom styling with gradients and animations
- **JavaScript** - Interactive features
- **Bootstrap 5** - Responsive UI framework
- **jQuery** - AJAX and DOM manipulation

### Database
- **SQLite** - Default database (configurable)

## 📋 Prerequisites

- Python 3.11 or higher
- Webcam (for face capture and recognition)
- Modern web browser (Chrome, Firefox, Edge)

## 🚀 Installation & Setup

### 1. Clone or Download the Project

```bash
cd Face_Attendance_System
```

### 2. Create Virtual Environment

```bash
python -m venv venv
```

### 3. Activate Virtual Environment

**Windows:**
```bash
venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create Superuser (Admin)

```bash
python manage.py createsuperuser
```

Follow the prompts to create an admin account:
- Username: admin
- Email: admin@example.com
- Password: (your secure password)

### 7. Run Development Server

```bash
python manage.py runserver
```

### 8. Access the Application

Open your browser and navigate to:
```
http://127.0.0.1:8000/
```

## 📖 Usage Guide

### For Administrators

#### 1. Login
- Navigate to `http://127.0.0.1:8000/`
- Login with your admin credentials

#### 2. Add New User
- Go to **Users** → **Add New User**
- Fill in user details (username, email, unique ID, etc.)
- Submit the form

#### 3. Capture Face Data
- Go to **Users** → Select a user → **Capture Face**
- Allow webcam access when prompted
- System will automatically capture 20 face samples
- Ensure good lighting and face the camera directly

#### 4. Train Face Recognition Model
- Go to **Train Model** from the navigation menu
- Click **Train Model** button
- Wait for training to complete
- Model will be saved as `models/face_model.yml`

#### 5. Mark Attendance
- Go to **Mark Attendance**
- Allow webcam access
- Click **Mark Attendance** button
- System will recognize face and mark attendance automatically

#### 6. View Reports
- **Daily Report**: View attendance for a specific date
- **Monthly Report**: View attendance for a specific month
- **User Report**: View attendance for a specific user
- Export reports as CSV or Excel
- Send reports via email

### For Regular Users

#### 1. Login
- Login with your user credentials

#### 2. View Dashboard
- See your attendance statistics
- View recent attendance records

#### 3. Mark Attendance
- Go to **Mark Attendance**
- Face the camera and click **Mark Attendance**

#### 4. View History
- Go to **History** to see all your attendance records

## 🏗️ Project Structure

```
Face_Attendance_System/
├── Face_Attendance_System/     # Project settings
│   ├── settings.py             # Django settings
│   ├── urls.py                 # Main URL configuration
│   └── wsgi.py                 # WSGI configuration
├── accounts/                   # Authentication app
│   ├── models.py               # Custom User model
│   ├── views.py                # Login/Logout views
│   └── forms.py                # Authentication forms
├── users/                      # User management app
│   ├── models.py               # UserProfile model
│   ├── views.py                # CRUD operations
│   └── templates/              # User templates
├── face_recognition_app/       # Face recognition core
│   ├── face_utils.py           # OpenCV utilities
│   ├── views.py                # Face capture/recognition
│   └── models.py               # FaceData model
├── attendance/                 # Attendance management
│   ├── models.py               # Attendance model
│   ├── views.py                # Attendance views
│   ├── reports.py              # Report generation
│   └── templates/              # Attendance templates
├── dashboard/                  # Dashboard app
│   ├── views.py                # Admin/User dashboards
│   └── templates/              # Dashboard templates
├── static/                     # Static files
│   ├── css/                    # Stylesheets
│   └── js/                     # JavaScript files
├── templates/                  # Base templates
│   └── base.html               # Base template
├── media/                      # Media files
│   └── faces/                  # Face datasets
├── models/                     # Trained ML models
│   └── face_model.yml          # LBPH model
├── haarcascades/               # Haar Cascade classifiers
├── requirements.txt            # Python dependencies
├── manage.py                   # Django management script
└── README.md                   # This file
```

## 🧠 Algorithms Used

### 1. Haar Cascade Classifier
- **Purpose**: Face detection in images/video frames
- **Method**: Uses cascade of simple features to detect faces
- **Advantages**: Fast, real-time detection
- **File**: `haarcascade_frontalface_default.xml`

### 2. LBPH Face Recognizer
- **Purpose**: Face recognition and identification
- **Method**: Local Binary Patterns Histograms
- **Advantages**: 
  - Robust to lighting variations
  - Good accuracy with small datasets
  - Fast training and prediction
- **Confidence Threshold**: 50 (lower is better)

## ⚙️ Configuration

### Email Settings
To enable email report delivery, configure the following in `settings.py`:

```python
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
```

Or set environment variables:
```bash
set EMAIL_HOST_USER=your-email@gmail.com
set EMAIL_HOST_PASSWORD=your-app-password
```

### Face Recognition Settings
Adjust in `settings.py`:

```python
CONFIDENCE_THRESHOLD = 50  # Lower is better for LBPH
NUM_FACE_SAMPLES = 20      # Number of samples per user
```

## 🔧 Troubleshooting

### Webcam Not Working
- Ensure webcam is connected and not used by another application
- Check browser permissions for camera access
- Try a different browser (Chrome recommended)

### Face Not Recognized
- Ensure face dataset is collected for the user
- Train the model after collecting face data
- Ensure good lighting conditions
- Face the camera directly
- Remove glasses if possible

### Model Training Fails
- Ensure at least one user has face data collected
- Check that face images are saved in `media/faces/`
- Verify OpenCV is installed correctly

## 📊 System Requirements

### Minimum Requirements
- **Processor**: Dual-core 2.0 GHz
- **RAM**: 4 GB
- **Storage**: 500 MB free space
- **Webcam**: 720p resolution
- **OS**: Windows 10/11, Linux, macOS

### Recommended Requirements
- **Processor**: Quad-core 2.5 GHz or higher
- **RAM**: 8 GB or more
- **Storage**: 1 GB free space
- **Webcam**: 1080p resolution

## 🚧 Limitations

1. **Lighting Dependency**: Performance degrades in poor lighting conditions
2. **Single Face**: Currently recognizes one face at a time
3. **Angle Sensitivity**: Works best with frontal face images
4. **Glasses/Accessories**: May affect recognition accuracy
5. **Database**: SQLite is suitable for small-scale deployments

## 🔮 Future Enhancements

- [ ] Multi-face recognition support
- [ ] Deep learning-based face recognition (FaceNet, ArcFace)
- [ ] Mobile application (Android/iOS)
- [ ] REST API for third-party integrations
- [ ] Real-time notifications
- [ ] Attendance analytics and insights
- [ ] PostgreSQL/MySQL support for production
- [ ] Docker containerization
- [ ] Cloud deployment (AWS, Azure, GCP)

## 📝 License

This project is created for educational purposes and college submission.

## 👨‍💻 Author

Face Recognition Attendance System
- **Technology**: Django + OpenCV
- **Year**: 2026

## 🙏 Acknowledgments

- Django Framework
- OpenCV Community
- Bootstrap Team
- Python Community

## 📞 Support

For issues or questions:
1. Check the troubleshooting section
2. Review the usage guide
3. Ensure all dependencies are installed correctly

---

**Note**: This system is designed for educational purposes and small-scale deployments. For production use, consider additional security measures, scalability improvements, and compliance with data protection regulations.
