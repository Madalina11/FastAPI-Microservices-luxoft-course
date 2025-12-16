from sqlalchemy import Column, String, Integer, Text, DateTime
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import declarative_base
from datetime import datetime
import uuid

Base = declarative_base()

# TODO: Complete the Question ORM model
class Question(Base):
    __tablename__ = "questions"

    # First three columns as reference:
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    topic = Column(String, nullable=False)
    name = Column(String, nullable=False)

    # TODO: Add remaining columns:
    question = Column(Text, nullable=False)
    options = Column(JSONB, nullable=False)
    correct_option = Column(Integer, nullable=False)
    explanation = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=True)
