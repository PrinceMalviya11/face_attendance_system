"""
Face Recognition Views
Handles face capture, training, and recognition
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import StreamingHttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
import cv2
import json
from accounts.models import CustomUser
from users.models import UserProfile
from .models import FaceData
from .face_utils import face_recognition_system


@login_required
def capture_face_view(request, user_id):
    """
    Capture face dataset for a user
    Admin only
    """
    if not request.user.is_admin():
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('dashboard:index')
    
    user = get_object_or_404(CustomUser, id=user_id)
    
    if request.method == 'POST':
        # Capture face dataset
        success, message, count = face_recognition_system.capture_face_dataset(
            user_id=user.id,
            num_samples=20
        )
        
        if success:
            # Update face data record
            face_data, created = FaceData.objects.get_or_create(user=user)
            face_data.dataset_collected = True
            face_data.samples_count = count
            face_data.save()
            
            # Update user profile
            profile, created = UserProfile.objects.get_or_create(user=user)
            profile.face_dataset_collected = True
            profile.face_samples_count = count
            profile.last_dataset_update = timezone.now()
            profile.save()
            
            messages.success(request, message)
        else:
            messages.error(request, message)
        
        return redirect('users:user_detail', user_id=user.id)
    
    return render(request, 'face_recognition_app/capture_face.html', {'user_obj': user})


@login_required
def train_model_view(request):
    """
    Train face recognition model
    Admin only
    """
    if not request.user.is_admin():
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('dashboard:index')
    
    if request.method == 'POST':
        try:
            import logging
            logger = logging.getLogger(__name__)
            logger.info("Starting face model training...")
            
            # Check if there's data to train
            users_with_data = FaceData.objects.filter(dataset_collected=True).count()
            if users_with_data == 0:
                messages.error(request, 'No users with face data found. Please collect face data first.')
                return redirect('face_recognition_app:train_model')
            
            # Train the model
            success, message, user_count = face_recognition_system.train_model()
            
            logger.info(f"Training result - Success: {success}, Message: {message}, Users: {user_count}")
            
            if success:
                messages.success(request, message)
                logger.info("Model training completed successfully")
            else:
                messages.error(request, message)
                logger.error(f"Model training failed: {message}")
            
        except Exception as e:
            import traceback
            error_msg = f"Error during model training: {str(e)}"
            logger.error(error_msg)
            logger.error(traceback.format_exc())
            messages.error(request, f"An error occurred during training: {str(e)}")
        
        return redirect('dashboard:admin_dashboard')
    
    # Get training statistics
    total_users = CustomUser.objects.count()
    users_with_data = FaceData.objects.filter(dataset_collected=True).count()
    
    # Check if model exists
    import os
    from django.conf import settings
    model_exists = os.path.exists(settings.FACE_MODEL_PATH)
    
    context = {
        'total_users': total_users,
        'users_with_data': users_with_data,
        'model_exists': model_exists,
    }
    
    return render(request, 'face_recognition_app/train_model.html', context)


def generate_frames():
    """
    Generator function for video streaming
    Detects faces in real-time
    """
    camera = cv2.VideoCapture(0)
    
    while True:
        success, frame = camera.read()
        if not success:
            break
        
        # Detect faces
        faces = face_recognition_system.detect_faces(frame)
        
        # Draw rectangles around faces
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(frame, "Face Detected", (x, y-10),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
        
        # Encode frame
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    
    camera.release()


@login_required
def video_feed(request):
    """
    Video streaming route for face detection
    """
    return StreamingHttpResponse(
        generate_frames(),
        content_type='multipart/x-mixed-replace; boundary=frame'
    )


@login_required
@csrf_exempt
def recognize_face_ajax(request):
    """
    AJAX endpoint for face recognition
    Returns recognized user information
    """
    if request.method == 'POST':
        # Capture frame from webcam
        camera = cv2.VideoCapture(0)
        ret, frame = camera.read()
        camera.release()
        
        if not ret:
            return JsonResponse({
                'success': False,
                'message': 'Failed to capture frame from webcam'
            })
        
        # Recognize face
        user_id, confidence, face_location = face_recognition_system.recognize_face(frame)
        
        if user_id is not None:
            try:
                user = CustomUser.objects.get(id=user_id)
                return JsonResponse({
                    'success': True,
                    'user_id': user.id,
                    'username': user.username,
                    'unique_id': user.unique_id,
                    'full_name': f"{user.first_name} {user.last_name}",
                    'confidence': float(confidence)
                })
            except CustomUser.DoesNotExist:
                return JsonResponse({
                    'success': False,
                    'message': 'User not found in database'
                })
        else:
            return JsonResponse({
                'success': False,
                'message': 'Face not recognized or confidence too low',
                'confidence': float(confidence) if confidence else None
            })
    
    return JsonResponse({'success': False, 'message': 'Invalid request method'})
