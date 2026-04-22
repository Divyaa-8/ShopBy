@echo off
echo.
echo  ==================================
echo   Shopzy Django Setup Script
echo  ==================================
echo.

REM Step 1 – Install dependencies
echo [1/4] Installing Django...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: pip failed. Make sure Python is installed!
    pause
    exit /b 1
)

REM Step 2 – Run migrations (creates the database)
echo.
echo [2/4] Setting up database...
python manage.py makemigrations
python manage.py migrate

REM Step 3 – Load sample products
echo.
echo [3/4] Loading sample products...
python manage.py loaddata store/fixtures/initial_data.json

REM Step 4 – Create admin user
echo.
echo [4/4] Creating admin account...
echo    Username: admin
echo    Password: admin123
python manage.py shell -c "from django.contrib.auth.models import User; User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@shopzy.com', 'admin123')"

echo.
echo  ======================================
echo   Setup complete! Now run:
echo     python manage.py runserver
echo   Then open: http://127.0.0.1:8000
echo   Admin panel: http://127.0.0.1:8000/admin
echo  ======================================
echo.
pause
