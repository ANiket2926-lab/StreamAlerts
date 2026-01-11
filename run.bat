@echo off
echo =====================================================
echo   StreamAlerts - Quick Start
echo =====================================================
echo.

:: Check if venv exists
if not exist "venv" (
    echo First run detected. Setting up environment...
    python -m venv venv
    call venv\Scripts\activate.bat
    pip install -r requirements.txt
) else (
    call venv\Scripts\activate.bat
)

echo Starting StreamAlerts...
echo.
python main.py
