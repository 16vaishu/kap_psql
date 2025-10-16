from fastapi import FastAPI, Depends, HTTPException, UploadFile, File
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
import models, schemas, crud
from database import engine, SessionLocal
import pandas as pd
import io

# Create all database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="PySQL Gym 🧠", description="Learn Python and SQL through interactive quizzes!")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Dependency for DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# 🏠 Home route - serve the frontend
@app.get("/")
def read_root():
    return FileResponse("static/index.html")


# 🧱 TOPIC ENDPOINTS
@app.post("/api/topics/", response_model=schemas.Topic)
def create_topic(topic: schemas.TopicCreate, db: Session = Depends(get_db)):
    return crud.create_topic(db=db, topic=topic)


@app.get("/api/topics/", response_model=list[schemas.Topic])
def read_topics(db: Session = Depends(get_db)):
    return crud.get_topics(db)


@app.get("/api/topics/{topic_id}", response_model=schemas.Topic)
def read_topic(topic_id: int, db: Session = Depends(get_db)):
    topic = crud.get_topic(db, topic_id=topic_id)
    if topic is None:
        raise HTTPException(status_code=404, detail="Topic not found")
    return topic


# ❓ QUIZ ENDPOINTS
@app.post("/api/quizzes/", response_model=schemas.Quiz)
def create_quiz(quiz: schemas.QuizCreate, db: Session = Depends(get_db)):
    # Check if topic exists
    topic = crud.get_topic(db, topic_id=quiz.topic_id)
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")
    return crud.create_quiz(db=db, quiz=quiz)


@app.get("/api/quizzes/topic/{topic_id}", response_model=list[schemas.Quiz])
def read_quizzes_by_topic(topic_id: int, db: Session = Depends(get_db)):
    return crud.get_quizzes_by_topic(db, topic_id=topic_id)


@app.get("/api/quizzes/{quiz_id}", response_model=schemas.Quiz)
def read_quiz(quiz_id: int, db: Session = Depends(get_db)):
    quiz = crud.get_quiz(db, quiz_id=quiz_id)
    if quiz is None:
        raise HTTPException(status_code=404, detail="Quiz not found")
    return quiz


# 🧾 SUBMISSION ENDPOINTS
@app.post("/api/submissions/", response_model=schemas.Submission)
def create_submission(submission: schemas.SubmissionCreate, db: Session = Depends(get_db)):
    db_submission = crud.create_submission(db=db, submission=submission)
    if db_submission is None:
        raise HTTPException(status_code=404, detail="Quiz not found")
    return db_submission


@app.get("/api/submissions/", response_model=list[schemas.Submission])
def read_submissions(db: Session = Depends(get_db)):
    return crud.get_submissions(db)


# 🎯 Initialize with sample data
@app.post("/api/init-data/")
def initialize_sample_data(db: Session = Depends(get_db)):
    """Initialize the database with sample topics and quizzes"""
    
    # Check if data already exists
    existing_topics = crud.get_topics(db)
    if existing_topics:
        return {"message": "Sample data already exists"}
    
    # Create sample topics
    python_topic = crud.create_topic(db, schemas.TopicCreate(
        title="Python Basics",
        description="Learn the fundamentals of Python programming"
    ))
    
    sql_topic = crud.create_topic(db, schemas.TopicCreate(
        title="SQL Fundamentals", 
        description="Master the basics of SQL database queries"
    ))
    
    # Create sample Python quizzes
    python_quizzes = [
        {
            "question": "What is the correct way to create a list in Python?",
            "choices": ["list = []", "list = ()", "list = {}", "list = <>"],
            "correct_answer": "list = []",
            "topic_id": python_topic.id
        },
        {
            "question": "Which keyword is used to define a function in Python?",
            "choices": ["function", "def", "func", "define"],
            "correct_answer": "def",
            "topic_id": python_topic.id
        },
        {
            "question": "What does 'len()' function do in Python?",
            "choices": ["Returns the length of an object", "Creates a new list", "Sorts a list", "Removes duplicates"],
            "correct_answer": "Returns the length of an object",
            "topic_id": python_topic.id
        }
    ]
    
    # Create sample SQL quizzes
    sql_quizzes = [
        {
            "question": "Which SQL statement is used to extract data from a database?",
            "choices": ["GET", "SELECT", "EXTRACT", "OPEN"],
            "correct_answer": "SELECT",
            "topic_id": sql_topic.id
        },
        {
            "question": "Which SQL clause is used to filter records?",
            "choices": ["FILTER", "WHERE", "HAVING", "CONDITION"],
            "correct_answer": "WHERE",
            "topic_id": sql_topic.id
        },
        {
            "question": "What does SQL stand for?",
            "choices": ["Structured Query Language", "Simple Query Language", "Standard Query Language", "System Query Language"],
            "correct_answer": "Structured Query Language",
            "topic_id": sql_topic.id
        }
    ]
    
    # Add all quizzes
    for quiz_data in python_quizzes + sql_quizzes:
        crud.create_quiz(db, schemas.QuizCreate(**quiz_data))
    
    return {"message": "Sample data initialized successfully!"}


# 📊 EXCEL UPLOAD ENDPOINT
@app.post("/api/upload-quizzes/", response_model=schemas.BulkQuizUploadResponse)
async def upload_quizzes_excel(
    file: UploadFile = File(...),
    topic_id: int = None,
    db: Session = Depends(get_db)
):
    """
    Upload quizzes from Excel file
    
    Expected Excel format:
    - Column A: Question
    - Column B: Choice 1
    - Column C: Choice 2
    - Column D: Choice 3
    - Column E: Choice 4
    - Column F: Correct Answer
    - Column G: Topic ID (optional if topic_id parameter is provided)
    """
    
    # Validate file type
    if not file.filename.endswith(('.xlsx', '.xls')):
        raise HTTPException(status_code=400, detail="File must be an Excel file (.xlsx or .xls)")
    
    try:
        # Read Excel file
        contents = await file.read()
        df = pd.read_excel(io.BytesIO(contents))
        
        # Validate required columns
        required_columns = ['Question', 'Choice 1', 'Choice 2', 'Choice 3', 'Choice 4', 'Correct Answer']
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            raise HTTPException(
                status_code=400, 
                detail=f"Missing required columns: {', '.join(missing_columns)}"
            )
        
        # Process each row
        quizzes_to_create = []
        errors = []
        
        for index, row in df.iterrows():
            try:
                # Get topic_id from parameter or Excel column
                row_topic_id = topic_id
                if 'Topic ID' in df.columns and pd.notna(row['Topic ID']):
                    row_topic_id = int(row['Topic ID'])
                
                if not row_topic_id:
                    errors.append(f"Row {index + 2}: No topic ID provided")
                    continue
                
                # Verify topic exists
                topic = crud.get_topic(db, topic_id=row_topic_id)
                if not topic:
                    errors.append(f"Row {index + 2}: Topic with ID {row_topic_id} not found")
                    continue
                
                # Validate required fields
                if pd.isna(row['Question']) or not str(row['Question']).strip():
                    errors.append(f"Row {index + 2}: Question is required")
                    continue
                
                if pd.isna(row['Correct Answer']) or not str(row['Correct Answer']).strip():
                    errors.append(f"Row {index + 2}: Correct Answer is required")
                    continue
                
                # Build choices list
                choices = []
                for i in range(1, 5):
                    choice_col = f'Choice {i}'
                    if choice_col in df.columns and pd.notna(row[choice_col]):
                        choice_value = str(row[choice_col]).strip()
                        if choice_value:
                            choices.append(choice_value)
                
                if len(choices) < 2:
                    errors.append(f"Row {index + 2}: At least 2 choices are required")
                    continue
                
                # Validate correct answer is in choices
                correct_answer = str(row['Correct Answer']).strip()
                if correct_answer not in choices:
                    errors.append(f"Row {index + 2}: Correct answer '{correct_answer}' must be one of the choices")
                    continue
                
                # Create quiz object
                quiz_create = schemas.QuizCreate(
                    question=str(row['Question']).strip(),
                    choices=choices,
                    correct_answer=correct_answer,
                    topic_id=row_topic_id
                )
                
                quizzes_to_create.append(quiz_create)
                
            except Exception as e:
                errors.append(f"Row {index + 2}: {str(e)}")
        
        # Create quizzes in bulk
        created_count = 0
        if quizzes_to_create:
            try:
                created_quizzes = crud.create_bulk_quizzes(db, quizzes_to_create)
                created_count = len(created_quizzes)
            except Exception as e:
                errors.append(f"Database error: {str(e)}")
        
        # Prepare response
        success = created_count > 0
        message = f"Successfully created {created_count} quizzes"
        if errors:
            message += f" with {len(errors)} errors"
        
        return schemas.BulkQuizUploadResponse(
            success=success,
            message=message,
            created_count=created_count,
            errors=errors
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")


# 📥 DOWNLOAD TEMPLATE ENDPOINT
@app.get("/api/download-template/")
def download_quiz_template():
    """Download Excel template for quiz upload"""
    
    # Create sample data for template
    template_data = {
        'Question': [
            'What is the correct way to create a list in Python?',
            'Which keyword is used to define a function in Python?'
        ],
        'Choice 1': ['list = []', 'function'],
        'Choice 2': ['list = ()', 'def'],
        'Choice 3': ['list = {}', 'func'],
        'Choice 4': ['list = <>', 'define'],
        'Correct Answer': ['list = []', 'def'],
        'Topic ID': [1, 1]
    }
    
    df = pd.DataFrame(template_data)
    
    # Create Excel file in memory
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name='Quiz Template', index=False)
    
    output.seek(0)
    
    from fastapi.responses import StreamingResponse
    
    return StreamingResponse(
        io.BytesIO(output.read()),
        media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        headers={"Content-Disposition": "attachment; filename=quiz_template.xlsx"}
    )
