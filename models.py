from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, JSON
from sqlalchemy.orm import relationship
from database import Base

class Topic(Base):
    __tablename__ = "topics"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True, index=True)
    description = Column(String)

    quizzes = relationship("Quiz", back_populates="topic")


class Quiz(Base):
    __tablename__ = "quizzes"
    id = Column(Integer, primary_key=True, index=True)
    question = Column(String)
    choices = Column(JSON)  # Store multiple choice options as JSON
    correct_answer = Column(String)
    topic_id = Column(Integer, ForeignKey("topics.id"))

    topic = relationship("Topic", back_populates="quizzes")
    submissions = relationship("Submission", back_populates="quiz")


class Submission(Base):
    __tablename__ = "submissions"
    id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String)
    selected = Column(String)  # User's selected answer
    is_correct = Column(Boolean)
    score = Column(Integer, default=0)
    quiz_id = Column(Integer, ForeignKey("quizzes.id"))

    quiz = relationship("Quiz", back_populates="submissions")
