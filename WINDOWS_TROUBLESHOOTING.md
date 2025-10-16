# Windows Troubleshooting Guide

This guide helps resolve common issues when running PySQL Gym on Windows systems.

## Common Issues and Solutions

### 1. Static Files Not Loading (404 Errors)

**Symptoms:**
- Browser console shows errors like:
  ```
  GET /assets/index-CrmkxDlo.js HTTP/1.1" 404 Not Found
  GET /assets/index-C4Lpm2yl.css HTTP/1.1" 404 Not Found
  ```

**Causes:**
- Browser cache from a different version
- Path resolution issues on Windows
- Build artifacts from a different project

**Solutions:**

#### Solution 1: Clear Browser Cache
1. **Hard Refresh:** Press `Ctrl + F5` or `Ctrl + Shift + R`
2. **Clear Cache:** 
   - Chrome: `Ctrl + Shift + Delete` → Clear browsing data
   - Firefox: `Ctrl + Shift + Delete` → Clear recent history
   - Edge: `Ctrl + Shift + Delete` → Clear browsing data

#### Solution 2: Use Incognito/Private Mode
- Open the application in an incognito/private browser window
- This bypasses any cached files

#### Solution 3: Debug Static Files
1. Visit the debug endpoint: `http://localhost:8000/debug/static-files`
2. This will show you:
   - Current directory path
   - Static directory path
   - List of available static files
3. Verify that `index.html`, `script.js`, and `style.css` are listed

#### Solution 4: Manual File Check
1. Navigate to your project directory
2. Verify the `static/` folder exists and contains:
   - `index.html`
   - `script.js` 
   - `style.css`

### 2. Database Connection Issues

**Symptoms:**
- 500 Internal Server Error on API calls
- "Failed to load topics" in browser console

**Solutions:**

#### For Local Development (Recommended)
1. **Install PostgreSQL locally:**
   - Download from: https://www.postgresql.org/download/windows/
   - Or use PostgreSQL portable version

2. **Update .env file:**
   ```env
   POSTGRES_USER=postgres
   POSTGRES_PASSWORD=your_local_password
   POSTGRES_HOST=localhost
   POSTGRES_PORT=5432
   POSTGRES_DB=pysql_gym
   ```

#### Alternative: Use SQLite (No PostgreSQL needed)
1. **Create a new database.py file for SQLite:**
   ```python
   from sqlalchemy import create_engine
   from sqlalchemy.ext.declarative import declarative_base
   from sqlalchemy.orm import sessionmaker

   SQLALCHEMY_DATABASE_URL = "sqlite:///./pysql_gym.db"

   engine = create_engine(
       SQLALCHEMY_DATABASE_URL, 
       connect_args={"check_same_thread": False}
   )
   SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
   Base = declarative_base()
   ```

2. **Update requirements.txt:**
   - Remove `psycopg2-binary`
   - SQLite is included with Python

### 3. Port Already in Use

**Symptoms:**
- Error: "Address already in use" when starting the server

**Solutions:**
1. **Find and kill the process:**
   ```cmd
   netstat -ano | findstr :8000
   taskkill /PID <PID_NUMBER> /F
   ```

2. **Use a different port:**
   ```cmd
   python -m uvicorn main:app --reload --host 0.0.0.0 --port 8001
   ```

### 4. Python Path Issues

**Symptoms:**
- ModuleNotFoundError when running the application

**Solutions:**
1. **Ensure you're in the correct directory:**
   ```cmd
   cd path\to\pysql_gym
   ```

2. **Use Python module execution:**
   ```cmd
   python -m uvicorn main:app --reload
   ```

3. **Check Python installation:**
   ```cmd
   python --version
   pip --version
   ```

### 5. Excel Upload Issues

**Symptoms:**
- Template download fails
- Excel upload returns errors

**Solutions:**
1. **Install required packages:**
   ```cmd
   pip install openpyxl pandas
   ```

2. **Check file permissions:**
   - Ensure the application has write permissions
   - Try running as administrator if needed

## Windows-Specific Setup

### 1. Using Windows Batch File
Create `start_windows.bat`:
```batch
@echo off
echo Starting PySQL Gym...
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
pause
```

### 2. Using PowerShell
Create `start_windows.ps1`:
```powershell
Write-Host "Starting PySQL Gym..." -ForegroundColor Green
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
Read-Host "Press Enter to exit"
```

### 3. Environment Variables
Set environment variables in Windows:
```cmd
set POSTGRES_USER=postgres
set POSTGRES_PASSWORD=your_password
set POSTGRES_HOST=localhost
set POSTGRES_PORT=5432
set POSTGRES_DB=pysql_gym
python -m uvicorn main:app --reload
```

## Testing Your Setup

### 1. Basic Functionality Test
1. Start the server: `python -m uvicorn main:app --reload`
2. Open browser: `http://localhost:8000`
3. Check debug endpoint: `http://localhost:8000/debug/static-files`
4. Try initializing sample data

### 2. Static Files Test
1. Verify CSS is loading (page should be styled)
2. Verify JavaScript is working (buttons should be interactive)
3. Check browser developer tools for any 404 errors

### 3. Database Test
1. Click "Initialize Sample Data"
2. Check if topics appear in the dropdown
3. Try taking a quiz

## Getting Help

If you're still experiencing issues:

1. **Check the debug endpoint:** `http://localhost:8000/debug/static-files`
2. **Check browser developer tools:** F12 → Console tab
3. **Check server logs:** Look at the terminal where uvicorn is running
4. **Create an issue:** Include error messages and system information

## System Requirements

- **Windows 10/11** (recommended)
- **Python 3.8+**
- **Modern web browser** (Chrome, Firefox, Edge)
- **PostgreSQL** (optional, can use SQLite)
- **4GB RAM** (minimum)
- **1GB free disk space**

## Performance Tips

1. **Use SSD storage** for better database performance
2. **Close unnecessary applications** to free up memory
3. **Use local database** instead of remote for development
4. **Enable Windows Defender exclusions** for the project folder
