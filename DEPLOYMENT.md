# 🚀 PySQL Gym Deployment Guide

This guide will help you deploy the PySQL Gym application on any machine with proper database setup.

## 📋 Prerequisites

- Docker and Docker Compose installed
- OR Python 3.11+ and PostgreSQL installed locally

## 🐳 Option 1: Docker Deployment (Recommended)

This is the easiest way to deploy the application with all dependencies.

### Step 1: Clone and Navigate
```bash
cd pysql_gym-main
```

### Step 2: Update Environment Variables
Edit the `docker-compose.yml` file and replace `your_password_here` with a secure password:

```yaml
environment:
  POSTGRES_PASSWORD: your_secure_password_123
```

### Step 3: Build and Run
```bash
# Build and start all services
docker-compose up --build

# Or run in background
docker-compose up --build -d
```

### Step 4: Access the Application
- Open your browser and go to: `http://localhost:8080`
- Click "Initialize Sample Data" to load sample quizzes
- Start learning!

### Step 5: Stop the Application
```bash
# Stop all services
docker-compose down

# Stop and remove volumes (this will delete all data)
docker-compose down -v
```

## 💻 Option 2: Local Development Setup

If you prefer to run without Docker:

### Step 1: Install Dependencies
```bash
# Install Python dependencies
pip install -r requirements.txt
```

### Step 2: Setup PostgreSQL Database
1. Install PostgreSQL on your system
2. Create a database named `pysql_gym`
3. Update the `.env` file with your database credentials:

```env
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_password
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=pysql_gym
```

### Step 3: Run the Application
```bash
# Start the FastAPI server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Step 4: Access the Application
- Open your browser and go to: `http://localhost:8000`
- Click "Initialize Sample Data" to load sample quizzes

## 🌐 Production Deployment

### Google Cloud Run Deployment

1. **Build and Push Docker Image**:
```bash
# Build for production
docker build -t gcr.io/YOUR_PROJECT_ID/pysql-gym .

# Push to Google Container Registry
docker push gcr.io/YOUR_PROJECT_ID/pysql-gym
```

2. **Setup Cloud SQL PostgreSQL**:
   - Create a Cloud SQL PostgreSQL instance
   - Create a database named `pysql_gym`
   - Note the connection details

3. **Deploy to Cloud Run**:
```bash
gcloud run deploy pysql-gym \
  --image gcr.io/YOUR_PROJECT_ID/pysql-gym \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars POSTGRES_HOST=YOUR_CLOUD_SQL_IP,POSTGRES_USER=postgres,POSTGRES_PASSWORD=YOUR_PASSWORD,POSTGRES_DB=pysql_gym
```

### AWS ECS/Fargate Deployment

1. **Push to ECR**:
```bash
# Create ECR repository
aws ecr create-repository --repository-name pysql-gym

# Build and push
docker build -t pysql-gym .
docker tag pysql-gym:latest YOUR_ACCOUNT.dkr.ecr.REGION.amazonaws.com/pysql-gym:latest
docker push YOUR_ACCOUNT.dkr.ecr.REGION.amazonaws.com/pysql-gym:latest
```

2. **Setup RDS PostgreSQL**:
   - Create an RDS PostgreSQL instance
   - Configure security groups for access

3. **Deploy with ECS/Fargate**:
   - Create ECS cluster
   - Create task definition with environment variables
   - Create service and deploy

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `POSTGRES_USER` | Database username | postgres |
| `POSTGRES_PASSWORD` | Database password | (required) |
| `POSTGRES_HOST` | Database host | localhost |
| `POSTGRES_PORT` | Database port | 5432 |
| `POSTGRES_DB` | Database name | pysql_gym |

### Database Schema

The application automatically creates the following tables:
- `topics` - Quiz topics (Python, SQL, etc.)
- `quizzes` - Individual quiz questions
- `submissions` - User quiz submissions and scores

## 🎯 API Endpoints

Once deployed, you can access the API documentation at:
- Swagger UI: `http://your-domain/docs`
- ReDoc: `http://your-domain/redoc`

## 🔍 Troubleshooting

### Common Issues

1. **Database Connection Error**:
   - Check if PostgreSQL is running
   - Verify environment variables
   - Check network connectivity

2. **Static Files Not Loading**:
   - Ensure the `static/` directory exists
   - Check file permissions

3. **Port Already in Use**:
   - Change the port in docker-compose.yml or uvicorn command
   - Kill existing processes using the port

### Logs

```bash
# Docker logs
docker-compose logs web
docker-compose logs db

# Follow logs in real-time
docker-compose logs -f web
```

## 🔒 Security Considerations

For production deployment:

1. **Use strong passwords** for database
2. **Enable HTTPS** with SSL certificates
3. **Configure CORS** properly for your domain
4. **Use environment variables** for sensitive data
5. **Regular backups** of the database
6. **Monitor logs** for suspicious activity

## 📊 Monitoring

Consider adding:
- Health check endpoints
- Application metrics
- Database monitoring
- Error tracking (Sentry, etc.)
- Performance monitoring

## 🔄 Updates and Maintenance

To update the application:

1. **Pull latest changes**
2. **Rebuild Docker images**
3. **Run database migrations** (if any)
4. **Restart services**

```bash
# Update with Docker
docker-compose down
docker-compose up --build -d
```

## 📞 Support

If you encounter issues:
1. Check the logs first
2. Verify environment configuration
3. Test database connectivity
4. Review the troubleshooting section

---

**Happy Deploying! 🚀**
