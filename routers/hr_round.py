from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import HrRound, HrRoundResponse
from schemas import HRQuestion, HRResponse
from typing import List

router = APIRouter()


@router.get("/questions", response_model=List[HRQuestion])
def get_hr_questions(db: Session = Depends(get_db)):
    questions = db.query(HrRound).order_by(HrRound.id).all()
    if not questions:
        raise HTTPException(status_code=404, detail="No HR questions found")
    return questions


@router.get("/responses/{task_id}", response_model=List[HRResponse])
def get_hr_responses(task_id: str, db: Session = Depends(get_db)):
    responses = db.query(HrRoundResponse).filter(HrRoundResponse.task_id == task_id).all()
    if not responses:
        raise HTTPException(status_code=404, detail="No HR responses found")
    return responses
