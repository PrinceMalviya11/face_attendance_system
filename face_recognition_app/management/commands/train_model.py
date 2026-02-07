"""
Management command to train the face recognition model
"""
from django.core.management.base import BaseCommand
from face_recognition_app.face_utils import face_recognition_system
from face_recognition_app.models import FaceData
from pathlib import Path
from django.conf import settings


class Command(BaseCommand):
    help = 'Train the face recognition model with collected face datasets'

    def add_arguments(self, parser):
        parser.add_argument(
            '--verbose',
            action='store_true',
            help='Show detailed training information',
        )

    def handle(self, *args, **options):
        verbose = options['verbose']
        
        self.stdout.write(self.style.WARNING('=' * 70))
        self.stdout.write(self.style.WARNING('FACE RECOGNITION MODEL TRAINING'))
        self.stdout.write(self.style.WARNING('=' * 70))
        
        # Check dataset
        dataset_path = Path(settings.FACE_DATASET_PATH)
        self.stdout.write(f'\n📁 Dataset Path: {dataset_path}')
        
        if not dataset_path.exists():
            self.stdout.write(self.style.ERROR('❌ Dataset directory does not exist!'))
            return
        
        # Count users with data
        users_with_data = FaceData.objects.filter(dataset_collected=True).count()
        self.stdout.write(f'👥 Users with face data: {users_with_data}')
        
        if users_with_data == 0:
            self.stdout.write(self.style.ERROR('❌ No users with face data found!'))
            self.stdout.write('Please collect face datasets first using the admin dashboard.')
            return
        
        # List user directories
        if verbose:
            self.stdout.write('\n📂 User directories:')
            for user_dir in dataset_path.iterdir():
                if user_dir.is_dir():
                    image_count = len(list(user_dir.glob("*.jpg")))
                    self.stdout.write(f'   - User {user_dir.name}: {image_count} images')
        
        # Train model
        self.stdout.write('\n🚀 Starting model training...')
        self.stdout.write('Please wait, this may take a few seconds...\n')
        
        try:
            success, message, user_count = face_recognition_system.train_model()
            
            if success:
                self.stdout.write(self.style.SUCCESS(f'✅ {message}'))
                
                # Verify model file
                model_path = Path(settings.FACE_MODEL_PATH)
                if model_path.exists():
                    size_kb = model_path.stat().st_size / 1024
                    self.stdout.write(f'📦 Model file: {model_path}')
                    self.stdout.write(f'📊 Model size: {size_kb:.2f} KB')
                else:
                    self.stdout.write(self.style.ERROR('⚠️  Warning: Model file not found after training!'))
            else:
                self.stdout.write(self.style.ERROR(f'❌ Training failed: {message}'))
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Error during training: {str(e)}'))
            if verbose:
                import traceback
                self.stdout.write(traceback.format_exc())
        
        self.stdout.write('\n' + '=' * 70)
        self.stdout.write(self.style.WARNING('TRAINING COMPLETE'))
        self.stdout.write('=' * 70)
