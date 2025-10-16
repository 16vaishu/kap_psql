# 🧠 PySQL Gym

A modern web application for learning Python and SQL through interactive quizzes!

## 🎯 What is PySQL Gym?

PySQL Gym is an educational web application that helps people learn Python and SQL programming through engaging multiple-choice quizzes. Think of it as your personal coding gym where you can exercise your programming knowledge!

### Features

- 📚 **Topic-based Learning**: Organized quizzes by topics (Python Basics, SQL Fundamentals, etc.)
- 🎮 **Interactive Quizzes**: Multiple-choice questions with instant feedback
- 📊 **Progress Tracking**: See your scores and review incorrect answers
- 🎨 **Modern UI**: Beautiful, responsive design that works on all devices
- 🚀 **Fast & Reliable**: Built with FastAPI for high performance

## 🏗️ Architecture

This project demonstrates a full-stack web application architecture:

- **Backend**: FastAPI (Python) - REST API server
- **Database**: PostgreSQL - Data storage
- **Frontend**: HTML, CSS, JavaScript - User interface
- **Containerization**: Docker - Easy deployment
- **Cloud Ready**: Designed for Google Cloud Run deployment

## 🛠️ Technology Stack

- **Python** - Backend programming language
- **FastAPI** - Modern web framework for building APIs
- **SQLAlchemy** - Database ORM (Object-Relational Mapping)
- **PostgreSQL** - Relational database
- **HTML/CSS/JavaScript** - Frontend technologies
- **Docker** - Containerization
- **Pydantic** - Data validation

## 📋 Prerequisites

Before running this application, make sure you have:

- Python 3.11 or higher
- PostgreSQL database
- Docker (optional, for containerized deployment)

## 🚀 Quick Start

### Option 1: Easy Startup (Recommended)

The easiest way to get started is using our startup script that automatically detects your system and chooses the best deployment method:

**For Linux/macOS:**
```bash
# Navigate to the project directory
cd pysql_gym-main

# Run the startup script
python start.py
# or
./start.py
```

**For Windows:**
```cmd
# Navigate to the project directory
cd pysql_gym-main

# Double-click start.bat or run in command prompt
start.bat
```

The startup script will:
- Check your system requirements
- Detect if Docker is available
- Check for PostgreSQL installation
- Guide you through the setup process
- Start the application automatically

### Option 2: Manual Setup

If you prefer manual setup:

#### With Docker (Includes Database)
```bash
# Update password in docker-compose.yml first
docker-compose up --build
```
Access at: `http://localhost:8080`

#### Without Docker (Requires PostgreSQL)
```bash
# Install dependencies
pip install -r requirements.txt

# Update .env with your database credentials
# Start PostgreSQL and create 'pysql_gym' database

# Run the application
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```
Access at: `http://localhost:8000`

### Initialize Sample Data

Once the application is running:
1. Open your browser and go to the application URL
2. Click "Initialize Sample Data" to load sample topics and quizzes
3. Start learning!

## 🐳 Docker Deployment

### Build and Run with Docker

```bash
# Build the Docker image
docker build -t pysql-gym .

# Run the container
docker run -p 8080:8080 pysql-gym
```

Access the application at: `http://localhost:8080`

## 📁 Project Structure

```
pysql_gym-main/
├── main.py              # FastAPI application and API endpoints
├── models.py            # Database models (SQLAlchemy)
├── schemas.py           # Pydantic schemas for data validation
├── crud.py              # Database operations
├── database.py          # Database configuration
├── requirements.txt     # Python dependencies
├── Dockerfile          # Docker configuration
├── .env                # Environment variables
├── static/             # Frontend files
│   ├── index.html      # Main HTML page
│   ├── style.css       # Styling
│   └── script.js       # JavaScript functionality
└── README.md           # This file
```

## 🔧 API Endpoints

### Topics
- `GET /api/topics/` - Get all topics
- `POST /api/topics/` - Create a new topic
- `GET /api/topics/{topic_id}` - Get a specific topic

### Quizzes
- `POST /api/quizzes/` - Create a new quiz
- `GET /api/quizzes/topic/{topic_id}` - Get quizzes for a topic
- `GET /api/quizzes/{quiz_id}` - Get a specific quiz

### Submissions
- `POST /api/submissions/` - Submit a quiz answer
- `GET /api/submissions/` - Get all submissions

### Utilities
- `POST /api/init-data/` - Initialize sample data

## 🎮 How to Use

1. **Start**: Open the application in your browser
2. **Initialize**: Click "Initialize Sample Data" to load sample quizzes
3. **Choose Topic**: Select a topic you want to practice
4. **Enter Name**: Provide your name to track your progress
5. **Take Quiz**: Answer the multiple-choice questions
6. **Review**: See your results and review incorrect answers
7. **Repeat**: Try again or choose a different topic

## 🌟 Learning Objectives

By building and using this application, you'll learn:

- **Backend Development**: FastAPI, REST APIs, database design
- **Frontend Development**: HTML, CSS, JavaScript, responsive design
- **Database Management**: PostgreSQL, SQLAlchemy ORM
- **DevOps**: Docker containerization, environment configuration
- **Full-Stack Integration**: How frontend and backend communicate

## 🚀 Deployment to Google Cloud Run

This application is designed to be easily deployed to Google Cloud Run:

1. Build and push Docker image to Google Container Registry
2. Deploy to Cloud Run with environment variables
3. Connect to Cloud SQL PostgreSQL instance

## 🤝 Contributing

Feel free to contribute to this project by:

- Adding new quiz topics
- Improving the UI/UX
- Adding new features
- Fixing bugs
- Writing tests

## 📝 License

This project is open source and available under the MIT License.

## 🎓 Educational Value

This project serves as an excellent learning resource for:

- **Beginners**: Learn web development concepts
- **Students**: Understand full-stack architecture
- **Developers**: Practice modern web technologies
- **Educators**: Use as a teaching tool

---

**Happy Learning! 🚀**

Built with ❤️ using FastAPI, PostgreSQL, and modern web technologies.
