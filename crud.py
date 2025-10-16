# crud.py
from sqlalchemy.orm import Session
import models, schemas

# Topics
def create_topic(db: Session, topic: schemas.TopicCreate):
    db_topic = models.Topic(title=topic.title, description=topic.description)
    db.add(db_topic)
    db.commit()
    db.refresh(db_topic)
    return db_topic

def get_topics(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Topic).offset(skip).limit(limit).all()

def get_topic(db: Session, topic_id: int):
    return db.query(models.Topic).filter(models.Topic.id == topic_id).first()

# Quizzes
def create_quiz(db: Session, quiz: schemas.QuizCreate):
    db_quiz = models.Quiz(
        topic_id=quiz.topic_id,
        question=quiz.question,
        choices=quiz.choices,
        correct_answer=quiz.correct_answer
    )
    db.add(db_quiz)
    db.commit()
    db.refresh(db_quiz)
    return db_quiz

def get_quizzes_by_topic(db: Session, topic_id: int):
    return db.query(models.Quiz).filter(models.Quiz.topic_id == topic_id).all()

def get_quiz(db: Session, quiz_id: int):
    return db.query(models.Quiz).filter(models.Quiz.id == quiz_id).first()

# Submissions
def create_submission(db: Session, submission: schemas.SubmissionCreate):
    quiz = get_quiz(db, submission.quiz_id)
    if not quiz:
        return None
    is_correct = (submission.selected == quiz.correct_answer)
    score = 1 if is_correct else 0
    db_sub = models.Submission(
        quiz_id=submission.quiz_id,
        user_name=submission.user_name,
        selected=submission.selected,
        is_correct=is_correct,
        score=score
    )
    db.add(db_sub)
    db.commit()
    db.refresh(db_sub)
    return db_sub

def get_submissions(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Submission).offset(skip).limit(limit).all()

def create_bulk_quizzes(db: Session, quizzes: list[schemas.QuizCreate]):
    """Create multiple quizzes in bulk"""
    created_quizzes = []
    for quiz in quizzes:
        db_quiz = models.Quiz(
            topic_id=quiz.topic_id,
            question=quiz.question,
            choices=quiz.choices,
            correct_answer=quiz.correct_answer
        )
        db.add(db_quiz)
        created_quizzes.append(db_quiz)
    
    db.commit()
    for quiz in created_quizzes:
        db.refresh(quiz)
    return created_quizzes
