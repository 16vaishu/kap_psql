# 🚀 PySQL Gym - Quick Start Guide

Choose the method that works best for your system:

## 🎯 Method 1: Smart Startup Script (Recommended)

**Linux/macOS:**
```bash
python start.py
```

**Windows:**
```cmd
start.bat
```

The script automatically detects your system and guides you through setup!

---

## 🐳 Method 2: Docker (Easiest - No Database Setup Required)

**Prerequisites:** Docker and Docker Compose installed

```bash
# Update password in docker-compose.yml
# Then run:
docker-compose up --build
```

**Access:** http://localhost:8080

---

## 💻 Method 3: Local Development (Requires PostgreSQL)

**Prerequisites:** Python 3.8+, PostgreSQL installed and running

```bash
# Install dependencies
pip install -r requirements.txt

# Update .env with your database credentials
# Create database 'pysql_gym' in PostgreSQL

# Run application
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Access:** http://localhost:8000

---

## 🌐 Method 4: Google Cloud Platform Deployment

**For GCP deployment with Docker:**

```bash
# Build for GCP
docker build -t gcr.io/YOUR_PROJECT_ID/pysql-gym .

# Push to Google Container Registry
docker push gcr.io/YOUR_PROJECT_ID/pysql-gym

# Deploy to Cloud Run
gcloud run deploy pysql-gym \
  --image gcr.io/YOUR_PROJECT_ID/pysql-gym \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars POSTGRES_HOST=YOUR_CLOUD_SQL_IP,POSTGRES_USER=postgres,POSTGRES_PASSWORD=YOUR_PASSWORD,POSTGRES_DB=pysql_gym
```

---

## 📋 After Starting the Application

1. **Open your browser** and go to the application URL
2. **Click "Initialize Sample Data"** to load sample quizzes
3. **Select a topic** (Python Basics or SQL Fundamentals)
4. **Enter your name** when prompted
5. **Start taking quizzes** and learning!

---

## 🔧 Environment Configuration

Update `.env` file for local development:

```env
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_password
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=pysql_gym
```

For Docker, update `docker-compose.yml`:

```yaml
environment:
  POSTGRES_PASSWORD: your_secure_password_123
```

---

## 🆘 Troubleshooting

**Database Connection Issues:**
- Ensure PostgreSQL is running
- Check credentials in `.env`
- Verify database `pysql_gym` exists

**Port Already in Use:**
- Change port in command or docker-compose.yml
- Kill existing processes: `lsof -ti:8000 | xargs kill -9`

**Dependencies Missing:**
```bash
pip install -r requirements.txt
```

**Docker Issues:**
```bash
docker-compose down
docker-compose up --build
```

---

## 📚 What You'll Learn

- **Python Programming**: Variables, functions, data structures
- **SQL Queries**: SELECT, WHERE, JOINs, and more
- **Web Development**: How modern web applications work
- **Database Design**: Relational database concepts
- **API Development**: REST API principles

---

**Need more help?** Check `DEPLOYMENT.md` for detailed instructions!

**Happy Learning! 🧠💪**
