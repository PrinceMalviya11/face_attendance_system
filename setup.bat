@echo off
echo ========================================
echo Face Recognition Attendance System
echo Setup Script
echo ========================================
echo.

echo [1/5] Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo Error: Failed to install dependencies
    pause
    exit /b 1
)
echo Dependencies installed successfully!
echo.

echo [2/5] Running migrations...
python manage.py makemigrations
if errorlevel 1 (
    echo Error: Failed to create migrations
    pause
    exit /b 1
)

python manage.py migrate
if errorlevel 1 (
    echo Error: Failed to apply migrations
    pause
    exit /b 1
)
echo Migrations completed successfully!
echo.

echo [3/5] Creating superuser...
echo Please enter admin credentials:
python manage.py createsuperuser
if errorlevel 1 (
    echo Error: Failed to create superuser
    pause
    exit /b 1
)
echo.

echo [4/5] Collecting static files...
python manage.py collectstatic --noinput
echo.

echo [5/5] Setup complete!
echo.
echo ========================================
echo Setup completed successfully!
echo ========================================
echo.
echo To start the server, run:
echo     python manage.py runserver
echo.
echo Then open your browser and go to:
echo     http://127.0.0.1:8000/
echo.
pause
