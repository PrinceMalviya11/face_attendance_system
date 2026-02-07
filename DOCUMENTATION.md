# Face Recognition Attendance System - Technical Documentation

## Table of Contents
1. [System Overview](#system-overview)
2. [System Architecture](#system-architecture)
3. [Algorithms Used](#algorithms-used)
4. [Hardware & Software Requirements](#hardware--software-requirements)
5. [Database Schema](#database-schema)
6. [API Endpoints](#api-endpoints)
7. [Security Features](#security-features)
8. [Limitations](#limitations)
9. [Future Enhancements](#future-enhancements)

---

## System Overview

The Face Recognition Attendance System is a web-based application that automates attendance marking using facial recognition technology. The system uses Django as the web framework and OpenCV for computer vision capabilities.

### Key Features
- Automated face detection and recognition
- Real-time attendance marking
- Role-based access control (Admin/User)
- Comprehensive reporting system
- Email-based report delivery
- Duplicate attendance prevention

---

## System Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        Client Layer                          │
│  (Web Browser - HTML/CSS/JavaScript/Bootstrap)              │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      │ HTTP/HTTPS
                      │
┌─────────────────────▼───────────────────────────────────────┐
│                    Application Layer                         │
│                    (Django Framework)                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │  Accounts    │  │    Users     │  │  Attendance  │     │
│  │    App       │  │     App      │  │     App      │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
│  ┌──────────────┐  ┌──────────────┐                        │
│  │ Face Recog.  │  │  Dashboard   │                        │
│  │    App       │  │     App      │                        │
│  └──────────────┘  └──────────────┘                        │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      │
┌─────────────────────▼───────────────────────────────────────┐
│                   Computer Vision Layer                      │
│                      (OpenCV)                                │
│  ┌──────────────────┐  ┌──────────────────┐                │
│  │  Haar Cascade    │  │  LBPH Recognizer │                │
│  │  Face Detection  │  │  Face Recognition│                │
│  └──────────────────┘  └──────────────────┘                │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      │
┌─────────────────────▼───────────────────────────────────────┐
│                     Data Layer                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   SQLite     │  │  Face Images │  │ Trained Model│     │
│  │  Database    │  │  (media/)    │  │  (models/)   │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└─────────────────────────────────────────────────────────────┘
```

### Component Description

#### 1. Accounts App
- **Purpose**: User authentication and authorization
- **Models**: CustomUser
- **Features**: Login, logout, role-based access

#### 2. Users App
- **Purpose**: User management
- **Models**: UserProfile
- **Features**: CRUD operations, profile management

#### 3. Face Recognition App
- **Purpose**: Core face recognition functionality
- **Models**: FaceData
- **Features**: Face detection, dataset collection, model training

#### 4. Attendance App
- **Purpose**: Attendance management and reporting
- **Models**: Attendance
- **Features**: Mark attendance, view history, generate reports

#### 5. Dashboard App
- **Purpose**: User interface and statistics
- **Features**: Admin dashboard, user dashboard, analytics

---

## Algorithms Used

### 1. Haar Cascade Classifier

**Purpose**: Face Detection

**How it works**:
- Uses cascade of simple features (Haar-like features)
- Trained on thousands of positive and negative images
- Detects faces in real-time from video frames

**Implementation**:
```python
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
faces = face_cascade.detectMultiScale(
    gray_image,
    scaleFactor=1.1,
    minNeighbors=5,
    minSize=(100, 100)
)
```

**Parameters**:
- `scaleFactor`: 1.1 (image pyramid scale)
- `minNeighbors`: 5 (minimum neighbors for detection)
- `minSize`: (100, 100) pixels

**Advantages**:
- Fast and efficient
- Real-time detection
- Low computational requirements

**Limitations**:
- Sensitive to face angle
- Requires frontal face view
- Affected by lighting conditions

### 2. LBPH Face Recognizer

**Purpose**: Face Recognition

**Full Name**: Local Binary Patterns Histograms

**How it works**:
1. Divides face image into small regions
2. Extracts LBP features from each region
3. Creates histogram for each region
4. Concatenates histograms to form feature vector
5. Compares feature vectors for recognition

**Implementation**:
```python
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.train(faces, labels)
recognizer.save('face_model.yml')

label, confidence = recognizer.predict(face_image)
```

**Parameters**:
- `radius`: 1 (default)
- `neighbors`: 8 (default)
- `grid_x`: 8 (default)
- `grid_y`: 8 (default)

**Confidence Threshold**: 50
- Lower confidence = better match
- Values below 50 are considered valid matches

**Advantages**:
- Robust to lighting variations
- Works well with small datasets
- Fast training and prediction
- Simple to implement

**Limitations**:
- Less accurate than deep learning methods
- Sensitive to facial expressions
- Requires multiple training samples

---

## Hardware & Software Requirements

### Minimum Requirements

**Hardware**:
- Processor: Intel Core i3 or equivalent (2.0 GHz)
- RAM: 4 GB
- Storage: 500 MB free space
- Webcam: 720p (1280x720)
- Display: 1366x768 resolution

**Software**:
- Operating System: Windows 10/11, Linux, macOS
- Python: 3.11 or higher
- Web Browser: Chrome 90+, Firefox 88+, Edge 90+

### Recommended Requirements

**Hardware**:
- Processor: Intel Core i5 or equivalent (2.5 GHz+)
- RAM: 8 GB or more
- Storage: 1 GB free space
- Webcam: 1080p (1920x1080)
- Display: 1920x1080 resolution

**Software**:
- Operating System: Windows 11, Ubuntu 22.04+
- Python: 3.11
- Web Browser: Latest Chrome or Firefox

---

## Database Schema

### CustomUser Table
```sql
CREATE TABLE accounts_customuser (
    id INTEGER PRIMARY KEY,
    username VARCHAR(150) UNIQUE NOT NULL,
    email VARCHAR(254) NOT NULL,
    password VARCHAR(128) NOT NULL,
    first_name VARCHAR(150),
    last_name VARCHAR(150),
    unique_id VARCHAR(50) UNIQUE NOT NULL,
    role VARCHAR(10) DEFAULT 'USER',
    phone VARCHAR(15),
    department VARCHAR(100),
    is_active BOOLEAN DEFAULT TRUE,
    is_staff BOOLEAN DEFAULT FALSE,
    is_superuser BOOLEAN DEFAULT FALSE,
    created_at DATETIME,
    updated_at DATETIME
);
```

### UserProfile Table
```sql
CREATE TABLE users_userprofile (
    id INTEGER PRIMARY KEY,
    user_id INTEGER UNIQUE REFERENCES accounts_customuser(id),
    profile_image VARCHAR(100),
    address TEXT,
    date_of_birth DATE,
    face_dataset_collected BOOLEAN DEFAULT FALSE,
    face_samples_count INTEGER DEFAULT 0,
    last_dataset_update DATETIME,
    created_at DATETIME,
    updated_at DATETIME
);
```

### FaceData Table
```sql
CREATE TABLE face_recognition_app_facedata (
    id INTEGER PRIMARY KEY,
    user_id INTEGER UNIQUE REFERENCES accounts_customuser(id),
    dataset_collected BOOLEAN DEFAULT FALSE,
    samples_count INTEGER DEFAULT 0,
    last_updated DATETIME,
    created_at DATETIME
);
```

### Attendance Table
```sql
CREATE TABLE attendance_attendance (
    id INTEGER PRIMARY KEY,
    user_id INTEGER REFERENCES accounts_customuser(id),
    date DATE NOT NULL,
    time TIME NOT NULL,
    status VARCHAR(10) DEFAULT 'PRESENT',
    subject VARCHAR(100),
    session VARCHAR(100),
    marked_by VARCHAR(50) DEFAULT 'Face Recognition',
    confidence REAL,
    created_at DATETIME,
    UNIQUE(user_id, date, session)
);
```

---

## Security Features

### 1. Authentication
- **Password Hashing**: PBKDF2 algorithm with SHA256
- **Session Management**: Django's built-in session framework
- **Login Protection**: CSRF tokens on all forms

### 2. Authorization
- **Role-Based Access**: Admin and User roles
- **Permission Checks**: Decorators on sensitive views
- **URL Protection**: Login required for all authenticated pages

### 3. Data Protection
- **Input Validation**: Form validation on all user inputs
- **SQL Injection Prevention**: Django ORM parameterized queries
- **XSS Protection**: Django template auto-escaping

### 4. Session Security
- **Session Timeout**: 24 hours
- **Secure Cookies**: HTTPOnly flag enabled
- **CSRF Protection**: Enabled on all POST requests

---

## Limitations

### Technical Limitations
1. **Single Face Recognition**: System recognizes one face at a time
2. **Lighting Dependency**: Performance degrades in poor lighting
3. **Angle Sensitivity**: Best results with frontal face view
4. **Glasses/Accessories**: May reduce recognition accuracy
5. **Database Scalability**: SQLite suitable for <1000 users

### Operational Limitations
1. **Internet Dependency**: Email reports require internet connection
2. **Webcam Requirement**: Mandatory for face capture and recognition
3. **Browser Compatibility**: Requires modern browser with webcam support
4. **Training Time**: Model retraining required for new users
5. **Storage**: Face images consume disk space (20 images per user)

### Performance Limitations
1. **Recognition Speed**: ~1-2 seconds per recognition
2. **Training Time**: Increases with number of users
3. **Concurrent Users**: Limited by server resources
4. **Video Streaming**: May lag on slow connections

---

## Future Enhancements

### Short-term (1-3 months)
- [ ] Multi-face recognition support
- [ ] Mobile responsive design improvements
- [ ] Attendance analytics dashboard
- [ ] Export reports in PDF format
- [ ] Bulk user import via CSV

### Medium-term (3-6 months)
- [ ] Deep learning-based recognition (FaceNet)
- [ ] REST API for mobile apps
- [ ] Real-time notifications
- [ ] PostgreSQL/MySQL support
- [ ] Advanced reporting with charts

### Long-term (6-12 months)
- [ ] Mobile application (Android/iOS)
- [ ] Cloud deployment support
- [ ] Biometric integration
- [ ] Multi-language support
- [ ] Advanced analytics with ML

---

## Conclusion

The Face Recognition Attendance System provides a robust, scalable solution for automated attendance management. Built with industry-standard technologies and following best practices, the system is suitable for educational institutions and small to medium-sized organizations.

For support and updates, refer to the README.md file.

---

**Document Version**: 1.0  
**Last Updated**: February 2026  
**Author**: Face Recognition Attendance System Team
