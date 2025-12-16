from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
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
    """Schema for creating a new question (no id or timestamps)"""
    pass

class Question(QuestionBase):
    """Schema for Question responses (includes id and timestamps)"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None

    # Allows creating Pydantic model from SQLAlchemy ORM object
    model_config = ConfigDict(from_attributes=True)
