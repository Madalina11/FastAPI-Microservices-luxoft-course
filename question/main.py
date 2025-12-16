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

@app.post("/questions/", response_model=QuestionSchema, status_code=status.HTTP_201_CREATED)
async def create_question(
    q: QuestionCreate,
    session: AsyncSession = Depends(get_async_session)
):
    # Creează obiectul ORM din datele primite de la API
    new_question = QuestionORM(**q.dict())

    # Adaugă în sesiune și salvează în baza de date
    session.add(new_question)
    await session.commit()

    # Reîncarcă obiectul din DB (ex. pentru created_at, id)
    await session.refresh(new_question)

    return new_question


# TODO: Implement READ ALL endpoint
# GET /questions/
# - Build query with select(QuestionORM)
# - Execute with await session.execute(query)
# - Extract results with result.scalars().all()
# - Return list of questions


# Get question by ID (REFERENCE IMPLEMENTATION)
@app.get("/questions/", response_model=List[QuestionSchema])
async def list_questions(
    session: AsyncSession = Depends(get_async_session)
):
    # Construiește query-ul pentru toate întrebările
    query = select(QuestionORM)

    # Rulează interogarea
    result = await session.execute(query)

    # Ia lista de obiecte ORM
    questions = result.scalars().all()

    return questions



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

@app.delete("/questions/{question_id}")
async def delete_question(
    question_id: str,
    session: AsyncSession = Depends(get_async_session)
):
    # Caută întrebarea după ID
    q = await session.get(QuestionORM, question_id)
    if not q:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Question not found"
        )

    # Șterge și confirmă în DB
    await session.delete(q)
    await session.commit()

    return {"detail": "Question deleted"}
