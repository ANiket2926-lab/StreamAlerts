@echo off
echo =====================================================
echo   StreamAlerts Build Script
echo   Building Windows Executable
echo =====================================================
echo.

:: Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    pause
    exit /b 1
)

:: Create virtual environment if it doesn't exist
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

:: Activate virtual environment
call venv\Scripts\activate.bat

:: Install dependencies
echo.
echo Installing dependencies...
pip install -r requirements.txt
pip install pyinstaller

:: Build executable
echo.
echo Building executable...
pyinstaller StreamAlerts.spec --clean

echo.
echo =====================================================
echo   Build Complete!
echo   Executable: dist\StreamAlerts.exe
echo =====================================================
pause
