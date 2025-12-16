from fastapi import FastAPI, HTTPException
from schemas.question import QuestionCreate, QuestionBase, Question as QuestionSchema
from database.question import quest_db, questions_table, QuestionQuery
from typing import List
import json
from datetime import datetime

# -----------------------------
# FastAPI setup
# -----------------------------
app = FastAPI(title="Quiz Service - Questions API")

@app.on_event("shutdown")
def shutdown_db_client():
    print("Closing TinyDB connection...")
    quest_db.close()  # This flushes all cached data to disk
    print("TinyDB closed.")

# -----------------------------
# CRUD Endpoints
# -----------------------------

# Create question
@app.post("/questions/", response_model=QuestionSchema)
def create_question(q: QuestionCreate):
    new_q = QuestionSchema(**q.dict())
    questions_table.insert(json.loads(new_q.json()))
    return new_q

@app.get("/questions/", response_model=List[QuestionSchema])
def list_questions():
    qs = questions_table.all()
    return qs

# Get question by ID
@app.get("/questions/{question_id}", response_model=QuestionSchema)
def get_question(question_id: str):
    q = questions_table.get(QuestionQuery.id == question_id)
    if not q:
        raise HTTPException(status_code=404, detail="Question not found")
    return q

# Update question
@app.put("/questions/{question_id}", response_model=QuestionSchema)
def update_question(question_id: str, q_update: QuestionCreate):
    q = questions_table.get(QuestionQuery.id == question_id)
    if not q:
        raise HTTPException(status_code=404, detail="Question not found")

    updated = QuestionSchema(
        **q_update.dict(),
        id=question_id,
        created_at=q["created_at"],
        updated_at=datetime.utcnow()
    )
    questions_table.update(updated.dict(), QuestionQuery.id == question_id)
    return updated

# Get question by ID
@app.delete("/questions/{question_id}")
def get_question(question_id: str):
    q = questions_table.get(QuestionQuery.id == question_id)
    if not q:
        raise HTTPException(status_code=404, detail="Question not found")    
    questions_table.remove(QuestionQuery.id == question_id)
    return {"detail", "question deleted"}

# Flush database
@app.post("/flush")
def flush_db():
    quest_db.storage.flush()
    return {"detail": "DB flushed"}

# Truncate quest table
@app.post("/truncate")
def clear_questions():
    questions_table.truncate()
    return {"detail": "Question table reset"}
