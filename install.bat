@echo off
echo =====================================
echo GST Pro v2.0 Installation
echo =====================================
echo.
echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found!
    echo Please install Python 3.11+ from python.org
    echo Make sure to check "Add Python to PATH"
    pause
    exit /b 1
)

echo Python found
echo.
echo Installing required packages...
python -m pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Installation failed
    pause
    exit /b 1
)

echo.
echo =====================================
echo Installation Successful!
echo =====================================
echo.
echo To start GST Pro Server:
echo   Double-click run.bat
echo.
echo Default Login:
echo   Username: admin
echo   Password: admin123
echo.
pause