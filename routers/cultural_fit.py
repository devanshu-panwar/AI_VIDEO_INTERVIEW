from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import CulturalFit, CulturalRoundResponse
from schemas import CulturalQuestion, CulturalResponse as CulturalResponseSchema
from typing import List

router = APIRouter()


@router.get("/questions", response_model=List[CulturalQuestion])
def get_cultural_questions(db: Session = Depends(get_db)):
    questions = db.query(CulturalFit).order_by(CulturalFit.id).all()
    if not questions:
        raise HTTPException(status_code=404, detail="No cultural fit questions found")
    return questions


@router.get("/responses/{task_id}", response_model=List[CulturalResponseSchema])
def get_cultural_responses(task_id: str, db: Session = Depends(get_db)):
    responses = db.query(CulturalRoundResponse).filter(CulturalRoundResponse.task_id == task_id).all()
    if not responses:
        raise HTTPException(status_code=404, detail="No cultural fit responses found")
    return responses
