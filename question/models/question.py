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
    # - question: Text, nullable=False
    # - options: JSONB, nullable=False
    # - correct_option: Integer, nullable=False
    # - explanation: Text, nullable=False
    # - created_at: DateTime, default=datetime.utcnow
    # - updated_at: DateTime, nullable=True
