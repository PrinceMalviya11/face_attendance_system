"""
Face Recognition Utilities using OpenCV
Handles face detection, dataset collection, training, and recognition
"""
import cv2
import numpy as np
import os
from pathlib import Path
from django.conf import settings
from datetime import datetime


class FaceRecognitionSystem:
    """
    Core face recognition system using Haar Cascade and LBPH
    """
    
    def __init__(self):
        """Initialize face recognition system"""
        self.haar_cascade_path = str(settings.HAAR_CASCADE_PATH)
        self.face_cascade = None
        self.recognizer = None
        self.model_path = str(settings.FACE_MODEL_PATH)
        self.confidence_threshold = settings.CONFIDENCE_THRESHOLD
        
        # Load Haar Cascade
        self._load_haar_cascade()
    
    def _load_haar_cascade(self):
        """Load Haar Cascade classifier for face detection"""
        if os.path.exists(self.haar_cascade_path):
            self.face_cascade = cv2.CascadeClassifier(self.haar_cascade_path)
        else:
            # Use OpenCV's built-in cascade if custom one doesn't exist
            self.face_cascade = cv2.CascadeClassifier(
                cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
            )
    
    def detect_faces(self, frame):
        """
        Detect faces in a frame using Haar Cascade
        
        Args:
            frame: Input image frame (BGR format)
        
        Returns:
            List of face rectangles [(x, y, w, h), ...]
        """
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(100, 100),
            flags=cv2.CASCADE_SCALE_IMAGE
        )
        return faces
    
    def capture_face_dataset(self, user_id, num_samples=20):
        """
        Capture face dataset for a user using webcam
        
        Args:
            user_id: Unique user identifier
            num_samples: Number of face samples to capture
        
        Returns:
            tuple: (success, message, samples_captured)
        """
        # Create user directory
        user_dir = Path(settings.FACE_DATASET_PATH) / str(user_id)
        user_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize webcam
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            return False, "Failed to open webcam", 0
        
        count = 0
        captured = 0
        
        print(f"Starting face capture for user {user_id}...")
        
        while captured < num_samples:
            ret, frame = cap.read()
            if not ret:
                break
            
            # Detect faces
            faces = self.detect_faces(frame)
            
            # Process first detected face
            if len(faces) > 0:
                (x, y, w, h) = faces[0]
                
                # Extract face region
                face_roi = frame[y:y+h, x:x+w]
                
                # Resize to standard size
                face_roi = cv2.resize(face_roi, (200, 200))
                
                # Save every 3rd frame to get variety
                if count % 3 == 0:
                    filename = user_dir / f"face_{captured + 1}.jpg"
                    cv2.imwrite(str(filename), face_roi)
                    captured += 1
                    print(f"Captured {captured}/{num_samples}")
                
                count += 1
        
        cap.release()
        
        if captured >= num_samples:
            return True, f"Successfully captured {captured} face samples", captured
        else:
            return False, f"Only captured {captured}/{num_samples} samples", captured
    
    def train_model(self):
        """
        Train LBPH face recognizer with all collected face datasets
        
        Returns:
            tuple: (success, message, num_users_trained)
        """
        try:
            faces = []
            labels = []
            user_count = 0
            
            dataset_path = Path(settings.FACE_DATASET_PATH)
            
            # Validate dataset path
            if not dataset_path.exists():
                return False, "Face dataset directory not found. Please create face datasets first.", 0
            
            # Iterate through user directories
            for user_dir in dataset_path.iterdir():
                if user_dir.is_dir():
                    try:
                        user_id = int(user_dir.name)
                        user_images = 0
                        
                        # Load all face images for this user
                        for img_path in user_dir.glob("*.jpg"):
                            img = cv2.imread(str(img_path), cv2.IMREAD_GRAYSCALE)
                            if img is not None:
                                faces.append(img)
                                labels.append(user_id)
                                user_images += 1
                        
                        if user_images > 0:
                            user_count += 1
                            print(f"Loaded {user_images} images for user {user_id}")
                        
                    except ValueError:
                        print(f"Skipping invalid directory: {user_dir.name}")
                        continue
                    except Exception as e:
                        print(f"Error loading images from {user_dir.name}: {str(e)}")
                        continue
            
            # Validate we have data to train
            if len(faces) == 0:
                return False, "No face data found for training. Please collect face datasets first.", 0
            
            if user_count == 0:
                return False, "No valid user directories found. Please collect face datasets first.", 0
            
            print(f"Training with {len(faces)} face samples from {user_count} users...")
            
            # Create and train LBPH recognizer
            self.recognizer = cv2.face.LBPHFaceRecognizer_create()
            self.recognizer.train(faces, np.array(labels))
            
            # Save trained model
            model_dir = Path(self.model_path).parent
            model_dir.mkdir(parents=True, exist_ok=True)
            self.recognizer.save(self.model_path)
            
            # Verify model was saved
            if not Path(self.model_path).exists():
                return False, "Model training completed but failed to save model file.", user_count
            
            success_message = f"Model trained successfully with {user_count} users and {len(faces)} face samples"
            print(success_message)
            return True, success_message, user_count
            
        except cv2.error as e:
            error_msg = f"OpenCV error during training: {str(e)}"
            print(error_msg)
            return False, error_msg, 0
        except Exception as e:
            error_msg = f"Unexpected error during training: {str(e)}"
            print(error_msg)
            import traceback
            traceback.print_exc()
            return False, error_msg, 0
    
    def load_model(self):
        """
        Load trained face recognition model
        
        Returns:
            bool: True if model loaded successfully
        """
        if os.path.exists(self.model_path):
            self.recognizer = cv2.face.LBPHFaceRecognizer_create()
            self.recognizer.read(self.model_path)
            return True
        return False
    
    def recognize_face(self, frame):
        """
        Recognize face in a frame
        
        Args:
            frame: Input image frame (BGR format)
        
        Returns:
            tuple: (user_id, confidence, face_location) or (None, None, None)
        """
        if self.recognizer is None:
            if not self.load_model():
                return None, None, None
        
        # Detect faces
        faces = self.detect_faces(frame)
        
        if len(faces) == 0:
            return None, None, None
        
        # Process first detected face
        (x, y, w, h) = faces[0]
        face_roi = frame[y:y+h, x:x+w]
        
        # Convert to grayscale and resize
        gray_face = cv2.cvtColor(face_roi, cv2.COLOR_BGR2GRAY)
        gray_face = cv2.resize(gray_face, (200, 200))
        
        # Recognize face
        user_id, confidence = self.recognizer.predict(gray_face)
        
        # Check confidence threshold
        if confidence < self.confidence_threshold:
            return user_id, confidence, (x, y, w, h)
        else:
            return None, confidence, (x, y, w, h)
    
    def draw_face_rectangle(self, frame, face_location, label="", color=(0, 255, 0)):
        """
        Draw rectangle around detected face with label
        
        Args:
            frame: Input image frame
            face_location: Tuple (x, y, w, h)
            label: Text label to display
            color: Rectangle color (BGR)
        
        Returns:
            Modified frame with rectangle and label
        """
        if face_location is None:
            return frame
        
        x, y, w, h = face_location
        cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
        
        if label:
            cv2.putText(frame, label, (x, y-10), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)
        
        return frame


# Global instance for reuse
face_recognition_system = FaceRecognitionSystem()
