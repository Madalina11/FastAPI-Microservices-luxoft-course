from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from models.question import Question as QuestionORM
from schemas.question import QuestionCreate, QuestionBase, Question as QuestionSchema
from database.question import get_async_session, init_db
from typing import List
from datetime import datetime

# -----------------------------
# FastAPI setup
# -----------------------------
app = FastAPI(title="Quiz Service - Questions API")

@app.on_event("startup")
async def on_startup():
    """Initialize database tables on application startup"""
    await init_db()
    print("✅ Database initialized")

# -----------------------------
# CRUD Endpoints
# -----------------------------

# TODO: Implement CREATE endpoint
# POST /questions/
# - Accept QuestionCreate as input
# - Create QuestionORM instance
# - Add to session with session.add()
# - Commit with await session.commit()
# - Refresh with await session.refresh() to get DB-generated values
# - Return the created question


# TODO: Implement READ ALL endpoint
# GET /questions/
# - Build query with select(QuestionORM)
# - Execute with await session.execute(query)
# - Extract results with result.scalars().all()
# - Return list of questions


# Get question by ID (REFERENCE IMPLEMENTATION)
@app.get("/questions/{question_id}", response_model=QuestionSchema)
async def get_question(
    question_id: str,
    session: AsyncSession = Depends(get_async_session)
):
    """
    Retrieve a single question by ID.

    Key concepts:
    - session.get(): Fastest way to fetch by primary key
    - Checks session cache first, then queries database
    - Returns None if not found
    """
    q = await session.get(QuestionORM, question_id)
    if not q:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Question not found"
        )
    return q


# Update question (REFERENCE IMPLEMENTATION)
@app.put("/questions/{question_id}", response_model=QuestionSchema)
async def update_question(
    question_id: str,
    q_update: QuestionCreate,
    session: AsyncSession = Depends(get_async_session)
):
    """
    Update an existing question.

    Key concepts:
    - Fetch the existing question first
    - Update attributes using setattr() in a loop
    - SQLAlchemy tracks changes automatically (Unit of Work pattern)
    - No explicit UPDATE statement needed
    - Commit to persist changes
    - Refresh to get updated values from database
    """
    q = await session.get(QuestionORM, question_id)
    if not q:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Question not found"
        )

    # Update all fields from request
    for key, value in q_update.dict().items():
        setattr(q, key, value)

    # Update timestamp
    q.updated_at = datetime.utcnow()

    await session.commit()
    await session.refresh(q)
    return q


# TODO: Implement DELETE endpoint
# DELETE /questions/{question_id}
# - Fetch question by ID using session.get()
# - Check if exists (return 404 if not found)
# - Delete with await session.delete(q)
# - Commit with await session.commit()
# - Return success message {"detail": "Question deleted"}
