@echo off
REM PySQL Gym Startup Script for Windows
REM This script helps you run the PySQL Gym application

echo.
echo 🧠 PySQL Gym - Windows Startup Script
echo ================================
echo Learn Python and SQL through interactive quizzes!
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.8 or higher from https://python.org
    pause
    exit /b 1
)

echo ✅ Python is available

REM Check if requirements are installed
python -c "import fastapi, uvicorn, sqlalchemy, psycopg2, pydantic" >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Missing Python dependencies
    echo Installing dependencies...
    pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo ❌ Failed to install dependencies
        pause
        exit /b 1
    )
)

echo ✅ Python dependencies are available

REM Run the Python startup script
echo.
echo Starting PySQL Gym...
python start.py

pause
