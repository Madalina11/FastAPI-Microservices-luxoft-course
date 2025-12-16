from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
import uuid

class AnswerOption(BaseModel):
    num: int
    text: str

class QuestionBase(BaseModel):
    topic: str
    name: str
    question: str
    options: List[AnswerOption]
    correct_option: int
    explanation: str


class QuestionCreate(QuestionBase):
    pass

class Question(QuestionBase):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
