@echo off
title PySQL Gym - Starting Server
color 0A

echo.
echo ========================================
echo    🧠 PySQL Gym - Windows Launcher
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

echo ✅ Python found
python --version

REM Check if we're in the right directory
if not exist "main.py" (
    echo ❌ main.py not found
    echo Please run this script from the PySQL Gym project directory
    pause
    exit /b 1
)

echo ✅ Project files found

REM Check if virtual environment exists
if exist "venv\Scripts\activate.bat" (
    echo ✅ Virtual environment found, activating...
    call venv\Scripts\activate.bat
) else (
    echo ⚠️  No virtual environment found
    echo Consider creating one with: python -m venv venv
)

REM Install dependencies if needed
echo.
echo 📦 Checking dependencies...
pip install -r requirements.txt --quiet

REM Check if .env file exists
if not exist ".env" (
    echo.
    echo ⚠️  .env file not found
    echo Please copy .env.example to .env and configure your database settings
    echo.
    echo Would you like to create a basic .env file for local development? (y/n)
    set /p create_env=
    if /i "%create_env%"=="y" (
        echo Creating .env file for local development...
        (
            echo POSTGRES_USER=postgres
            echo POSTGRES_PASSWORD=password
            echo POSTGRES_HOST=localhost
            echo POSTGRES_PORT=5432
            echo POSTGRES_DB=pysql_gym
        ) > .env
        echo ✅ .env file created with default local settings
        echo Please update the password in .env file
    )
)

echo.
echo 🚀 Starting PySQL Gym server...
echo.
echo The application will be available at:
echo 📱 http://localhost:8000
echo 🔧 Debug info: http://localhost:8000/debug/static-files
echo.
echo Press Ctrl+C to stop the server
echo.

REM Start the server
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

echo.
echo Server stopped.
pause
