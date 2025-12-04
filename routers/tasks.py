from datetime import datetime
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import UserTask
from schemas import UserTaskCreate, UserTaskResponse

router = APIRouter()

@router.post("/generate_task", response_model=UserTaskResponse)
def generate_single_task(request: UserTaskCreate, db: Session = Depends(get_db)):

    # Generate unique timestamp part
    unique_part = datetime.utcnow().strftime("%Y-%m-%d-%H-%M")

    # Build task_id
    task_id = f"{request.u_id}_{request.type}_{unique_part}"

    # Create record
    new_task = UserTask(
        u_id=request.u_id,
        type=request.type,
        task_id=task_id
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task
