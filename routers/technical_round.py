from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import TechnicalRound, TechnicalRoundResponse
from schemas import TechnicalQuestion, TechnicalResponse as TechnicalResponseSchema
from typing import List
import random

router = APIRouter()


@router.get("/questions/{skill}", response_model=List[TechnicalQuestion])
def get_technical_questions(skill: str, db: Session = Depends(get_db)):
    skills = [s.strip().lower() for s in skill.split(",")]
    all_questions = []

    for s in skills:
        qset = db.query(TechnicalRound).filter(TechnicalRound.skill.ilike(s)).all()
        all_questions.extend(qset)

    if not all_questions:
        raise HTTPException(status_code=404, detail="No questions found for the given skills")

    random.shuffle(all_questions)
    return all_questions

@router.get("/questions/{skill}/{numQuestions}", response_model=List[TechnicalQuestion])
def get_technical_questions(skill: str, numQuestions: int, db: Session = Depends(get_db)):
    
    # Convert comma-separated skills → list
    # Example: "python,react" → ["python", "react"]
    skills = [s.strip().lower() for s in skill.split(",")]

    all_questions = []

    # Search each skill using ILIKE + wildcard (%)
    for s in skills:
        qset = db.query(TechnicalRound).filter(
            TechnicalRound.skill.ilike(f"%{s}%")   # 🔥 partial + case-insensitive
        ).all()

        all_questions.extend(qset)

    if not all_questions:
        raise HTTPException(
            status_code=404,
            detail="No questions found for the given skills."
        )

    # Shuffle randomly
    random.shuffle(all_questions)

    # Only return the number requested
    selected_questions = all_questions[:numQuestions]

    return selected_questions

@router.get("/responses/{task_id}", response_model=List[TechnicalResponseSchema])
def get_technical_responses(task_id: str, db: Session = Depends(get_db)):
    responses = db.query(TechnicalRoundResponse).filter(TechnicalRoundResponse.task_id == task_id).all()
    if not responses:
        raise HTTPException(status_code=404, detail="No responses found for this task")

    result = []
    for res in responses:
        q = db.query(TechnicalRound).filter(TechnicalRound.question == res.question).first()
        result.append({
            "task_id": res.task_id,
            "question": res.question,
            "transcript": res.transcript,
            "correct_answer": q.answer if q else "N/A"
        })
    return result
