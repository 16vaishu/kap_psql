# 🧠 PySQL Gym

An interactive web application for learning Python and SQL through engaging quizzes! Built with FastAPI, PostgreSQL, and vanilla JavaScript.

## ✨ Features

- **Interactive Quizzes**: Practice Python and SQL with multiple-choice questions
- **Topic-based Learning**: Organized quizzes by programming topics
- **Excel Upload**: Bulk upload quiz questions using Excel templates
- **Real-time Scoring**: Instant feedback and detailed results
- **User Progress Tracking**: Track quiz submissions and performance
- **Responsive Design**: Works seamlessly on desktop and mobile devices

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- PostgreSQL database (or SQLite for local development)
- pip (Python package manager)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/16vaishu/kap_psql.git
   cd kap_psql
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   
   Create a `.env` file in the root directory:
   ```env
   POSTGRES_USER=your_username
   POSTGRES_PASSWORD=your_password
   POSTGRES_HOST=your_host
   POSTGRES_PORT=5432
   POSTGRES_DB=your_database_name
   ```

4. **Run the application**
   
   **Linux/macOS:**
   ```bash
   python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```
   
   **Windows:**
   ```cmd
   # Option 1: Use the Windows launcher (recommended)
   start_windows.bat
   
   # Option 2: Manual command
   python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

5. **Access the application**
   
   Open your browser and navigate to: `http://localhost:8000`

### 🪟 Windows Users

For Windows users, we provide additional tools and troubleshooting:

- **Easy Launcher:** Double-click `start_windows.bat` to start the application
- **Troubleshooting:** See [WINDOWS_TROUBLESHOOTING.md](WINDOWS_TROUBLESHOOTING.md) for common issues
- **Debug Endpoint:** Visit `http://localhost:8000/debug/static-files` to check static file loading

**Common Windows Issues:**
- **Static files not loading:** Clear browser cache or use incognito mode
- **Database connection errors:** Use local PostgreSQL or SQLite (see troubleshooting guide)
- **Port conflicts:** The launcher will help you identify and resolve port issues

## 🐳 Docker Deployment

### Using Docker Compose

1. **Build and run with Docker Compose**
   ```bash
   docker-compose up --build
   ```

2. **Access the application**
   
   The app will be available at: `http://localhost:8000`

### Manual Docker Build

1. **Build the Docker image**
   ```bash
   docker build -t pysql-gym .
   ```

2. **Run the container**
   ```bash
   docker run -p 8000:8000 --env-file .env pysql-gym
   ```

## 📊 Usage

### Getting Started

1. **Initialize Sample Data**: Click the "Initialize Sample Data" button to populate the database with example topics and quizzes
2. **Choose a Topic**: Select from available programming topics (Python Basics, SQL Fundamentals, etc.)
3. **Take a Quiz**: Answer multiple-choice questions and get instant feedback
4. **View Results**: See your score and review correct answers

### Admin Features

#### Bulk Quiz Upload

1. **Download Template**: Get the Excel template with the correct format
2. **Fill Template**: Add your quiz questions following the template structure:
   - Column A: Question
   - Column B-E: Multiple choice options
   - Column F: Correct Answer
   - Column G: Topic ID (optional)
3. **Upload File**: Select topic and upload your Excel file
4. **Review Results**: Check upload status and any errors

#### Excel Template Format

| Question | Choice 1 | Choice 2 | Choice 3 | Choice 4 | Correct Answer | Topic ID |
|----------|----------|----------|----------|----------|----------------|----------|
| What is Python? | A programming language | A snake | A movie | A book | A programming language | 1 |

## 🏗️ Architecture

### Backend (FastAPI)

- **main.py**: Application entry point and API routes
- **models.py**: SQLAlchemy database models
- **schemas.py**: Pydantic data validation schemas
- **crud.py**: Database operations
- **database.py**: Database connection and configuration

### Frontend (Vanilla JavaScript)

- **index.html**: Main application interface
- **script.js**: Interactive functionality and API calls
- **style.css**: Responsive styling and animations

### Database Schema

#### Topics Table
- `id`: Primary key
- `title`: Topic name
- `description`: Topic description

#### Quizzes Table
- `id`: Primary key
- `topic_id`: Foreign key to topics
- `question`: Quiz question text
- `choices`: JSON array of answer choices
- `correct_answer`: The correct answer

#### Submissions Table
- `id`: Primary key
- `quiz_id`: Foreign key to quizzes
- `user_name`: Name of the quiz taker
- `selected`: User's selected answer
- `is_correct`: Boolean indicating if answer was correct
- `score`: Numeric score (1 for correct, 0 for incorrect)

## 🔧 API Endpoints

### Topics
- `GET /api/topics/`: List all topics
- `POST /api/topics/`: Create a new topic
- `GET /api/topics/{topic_id}`: Get specific topic

### Quizzes
- `GET /api/quizzes/topic/{topic_id}`: Get quizzes for a topic
- `POST /api/quizzes/`: Create a new quiz
- `GET /api/quizzes/{quiz_id}`: Get specific quiz

### Submissions
- `POST /api/submissions/`: Submit a quiz answer
- `GET /api/submissions/`: List all submissions

### Admin
- `POST /api/init-data/`: Initialize sample data
- `POST /api/upload-quizzes/`: Bulk upload quizzes from Excel
- `GET /api/download-template/`: Download Excel template

## 🛠️ Development

### Project Structure

```
pysql_gym/
├── main.py              # FastAPI application
├── models.py            # Database models
├── schemas.py           # Pydantic schemas
├── crud.py              # Database operations
├── database.py          # Database configuration
├── requirements.txt     # Python dependencies
├── Dockerfile           # Docker configuration
├── docker-compose.yml   # Docker Compose setup
├── .env                 # Environment variables (create this)
├── static/              # Frontend files
│   ├── index.html       # Main HTML file
│   ├── script.js        # JavaScript functionality
│   └── style.css        # Styling
└── README.md            # This file
```

### Adding New Features

1. **Database Changes**: Update `models.py` and create migrations
2. **API Endpoints**: Add routes in `main.py`
3. **Data Validation**: Update `schemas.py`
4. **Database Operations**: Add functions to `crud.py`
5. **Frontend**: Update HTML, CSS, and JavaScript files

### Running Tests

```bash
python test_app.py
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [FastAPI](https://fastapi.tiangolo.com/) for the backend API
- [PostgreSQL](https://www.postgresql.org/) for reliable data storage
- [SQLAlchemy](https://www.sqlalchemy.org/) for database ORM
- [Pandas](https://pandas.pydata.org/) for Excel file processing
- Vanilla JavaScript for lightweight frontend interactions

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/16vaishu/kap_psql/issues) page
2. Create a new issue with detailed information
3. Contact the maintainers

---

**Happy Learning! 🎓**
