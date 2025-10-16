#!/usr/bin/env python3
"""
PySQL Gym Startup Script
This script helps you run the PySQL Gym application with or without Docker.
"""

import os
import sys
import subprocess
import platform
import time
from pathlib import Path

def print_banner():
    """Print the application banner"""
    print("""
🧠 PySQL Gym - Startup Script
================================
Learn Python and SQL through interactive quizzes!
""")

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Error: Python 3.8 or higher is required")
        print(f"Current version: {sys.version}")
        sys.exit(1)
    print(f"✅ Python version: {sys.version.split()[0]}")

def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        import fastapi
        import uvicorn
        import sqlalchemy
        import psycopg2
        import pydantic
        print("✅ All Python dependencies are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Please install dependencies with: pip install -r requirements.txt")
        return False

def check_docker():
    """Check if Docker is available"""
    try:
        result = subprocess.run(['docker', '--version'], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print(f"✅ Docker available: {result.stdout.strip()}")
            return True
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    print("⚠️  Docker not available")
    return False

def check_docker_compose():
    """Check if Docker Compose is available"""
    try:
        result = subprocess.run(['docker-compose', '--version'], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print(f"✅ Docker Compose available: {result.stdout.strip()}")
            return True
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    
    # Try docker compose (newer syntax)
    try:
        result = subprocess.run(['docker', 'compose', 'version'], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print(f"✅ Docker Compose available: {result.stdout.strip()}")
            return True
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    
    print("⚠️  Docker Compose not available")
    return False

def check_postgresql():
    """Check if PostgreSQL is running locally"""
    try:
        import psycopg2
        from dotenv import load_dotenv
        
        load_dotenv()
        
        # Try to connect to PostgreSQL
        conn = psycopg2.connect(
            host=os.getenv('POSTGRES_HOST', 'localhost'),
            port=os.getenv('POSTGRES_PORT', '5432'),
            user=os.getenv('POSTGRES_USER', 'postgres'),
            password=os.getenv('POSTGRES_PASSWORD', ''),
            database='postgres'  # Connect to default database first
        )
        conn.close()
        print("✅ PostgreSQL is running and accessible")
        return True
    except Exception as e:
        print(f"⚠️  PostgreSQL connection failed: {e}")
        return False

def create_database_if_not_exists():
    """Create the application database if it doesn't exist"""
    try:
        import psycopg2
        from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
        from dotenv import load_dotenv
        
        load_dotenv()
        
        # Connect to PostgreSQL server
        conn = psycopg2.connect(
            host=os.getenv('POSTGRES_HOST', 'localhost'),
            port=os.getenv('POSTGRES_PORT', '5432'),
            user=os.getenv('POSTGRES_USER', 'postgres'),
            password=os.getenv('POSTGRES_PASSWORD', ''),
            database='postgres'
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        
        cursor = conn.cursor()
        db_name = os.getenv('POSTGRES_DB', 'pysql_gym')
        
        # Check if database exists
        cursor.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = %s", (db_name,))
        exists = cursor.fetchone()
        
        if not exists:
            cursor.execute(f'CREATE DATABASE "{db_name}"')
            print(f"✅ Created database: {db_name}")
        else:
            print(f"✅ Database already exists: {db_name}")
        
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"❌ Failed to create database: {e}")
        return False

def run_with_docker():
    """Run the application using Docker Compose"""
    print("\n🐳 Starting with Docker Compose...")
    
    if not os.path.exists('docker-compose.yml'):
        print("❌ docker-compose.yml not found!")
        return False
    
    try:
        # Try docker-compose first, then docker compose
        cmd = ['docker-compose', 'up', '--build']
        try:
            subprocess.run(['docker-compose', '--version'], 
                          capture_output=True, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            cmd = ['docker', 'compose', 'up', '--build']
        
        print("Starting services... (Press Ctrl+C to stop)")
        subprocess.run(cmd)
        return True
    except KeyboardInterrupt:
        print("\n🛑 Stopping services...")
        try:
            subprocess.run(['docker-compose', 'down'], timeout=30)
        except:
            subprocess.run(['docker', 'compose', 'down'], timeout=30)
        return True
    except Exception as e:
        print(f"❌ Failed to start with Docker: {e}")
        return False

def run_locally():
    """Run the application locally without Docker"""
    print("\n💻 Starting locally...")
    
    if not check_dependencies():
        return False
    
    if not check_postgresql():
        print("\n❌ PostgreSQL is required for local development.")
        print("Please install and start PostgreSQL, then update your .env file.")
        print("\nFor quick setup, you can:")
        print("1. Install PostgreSQL locally")
        print("2. Create a database named 'pysql_gym'")
        print("3. Update .env with your database credentials")
        return False
    
    if not create_database_if_not_exists():
        return False
    
    try:
        print("Starting FastAPI server... (Press Ctrl+C to stop)")
        print("Application will be available at: http://localhost:8000")
        
        # Start the server
        subprocess.run([
            sys.executable, '-m', 'uvicorn', 
            'main:app', 
            '--reload', 
            '--host', '0.0.0.0', 
            '--port', '8000'
        ])
        return True
    except KeyboardInterrupt:
        print("\n🛑 Server stopped")
        return True
    except Exception as e:
        print(f"❌ Failed to start server: {e}")
        return False

def main():
    """Main function"""
    print_banner()
    
    # Check Python version
    check_python_version()
    
    # Check what's available
    has_docker = check_docker()
    has_docker_compose = check_docker_compose()
    has_postgresql = check_postgresql()
    
    print("\n" + "="*50)
    print("DEPLOYMENT OPTIONS:")
    print("="*50)
    
    if has_docker and has_docker_compose:
        print("1. 🐳 Run with Docker (Recommended - includes database)")
    
    if has_postgresql:
        print("2. 💻 Run locally (Requires PostgreSQL)")
    elif not has_docker:
        print("2. 💻 Run locally (❌ PostgreSQL not detected)")
    
    if not has_docker and not has_postgresql:
        print("\n❌ No suitable deployment option available!")
        print("\nPlease either:")
        print("- Install Docker and Docker Compose, OR")
        print("- Install PostgreSQL and Python dependencies")
        sys.exit(1)
    
    print("\n" + "="*50)
    
    # Get user choice
    while True:
        if has_docker and has_docker_compose and has_postgresql:
            choice = input("Choose option (1 for Docker, 2 for Local, q to quit): ").strip().lower()
        elif has_docker and has_docker_compose:
            choice = input("Choose option (1 for Docker, q to quit): ").strip().lower()
        elif has_postgresql:
            choice = input("Choose option (2 for Local, q to quit): ").strip().lower()
        else:
            break
        
        if choice == 'q':
            print("👋 Goodbye!")
            sys.exit(0)
        elif choice == '1' and has_docker and has_docker_compose:
            success = run_with_docker()
            break
        elif choice == '2' and has_postgresql:
            success = run_locally()
            break
        else:
            print("Invalid choice. Please try again.")
    
    if 'success' in locals() and success:
        print("\n✅ Application started successfully!")
        print("\n📚 Next steps:")
        print("1. Open your browser and go to the application URL")
        print("2. Click 'Initialize Sample Data' to load sample quizzes")
        print("3. Start learning Python and SQL!")
    else:
        print("\n❌ Failed to start application")
        sys.exit(1)

if __name__ == "__main__":
    main()
