from pydantic import BaseModel
from typing import List, Optional

class QuizBase(BaseModel):
    question: str
    choices: List[str]
    correct_answer: str

class QuizCreate(QuizBase):
    topic_id: int

class Quiz(QuizBase):
    id: int
    topic_id: int

    class Config:
        orm_mode = True


class TopicBase(BaseModel):
    title: str
    description: Optional[str] = None

class TopicCreate(TopicBase):
    pass

class Topic(TopicBase):
    id: int
    quizzes: List[Quiz] = []

    class Config:
        orm_mode = True


class SubmissionBase(BaseModel):
    user_name: str
    selected: str

class SubmissionCreate(SubmissionBase):
    quiz_id: int

class Submission(SubmissionBase):
    id: int
    quiz_id: int
    is_correct: bool
    score: int

    class Config:
        orm_mode = True


class BulkQuizUploadResponse(BaseModel):
    success: bool
    message: str
    created_count: int
    errors: List[str] = []
