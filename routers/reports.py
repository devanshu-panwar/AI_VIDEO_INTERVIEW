from fastapi import APIRouter, Form, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from database import get_db
from services.gcp_helper import upload_to_gcp_bucket, bucket_name, read_text_from_gcp_bucket
from services.audio_processing import (
    generate_hr_report_with_gemini,
    generate_technical_report_with_gemini,
    generate_cultural_report_with_gemini
)
from models import HrRoundResponse, TechnicalRoundResponse, CulturalRoundResponse
import os

router = APIRouter()


# =====================================================
# HR REPORT
# =====================================================
@router.post("/hr")
def generate_hr_report(task_id: str = Form(...), db: Session = Depends(get_db)):
    responses = db.query(HrRoundResponse).filter(HrRoundResponse.task_id == task_id).all()
    if not responses:
        raise HTTPException(status_code=404, detail="No HR data found")

    qa_pairs = [
        {"question": r.question.question_text, "transcript": r.transcript}
        for r in responses
    ]

    report = generate_hr_report_with_gemini(qa_pairs)

    os.makedirs("Reports", exist_ok=True)
    local_path = f"Reports/{task_id}_hr.txt"
    with open(local_path, "w") as f:
        f.write(report)

    bucket_path = f"reports/{task_id}_hr.txt"
    upload_to_gcp_bucket(local_path, bucket_path)

    # OPTIONAL: delete local copy
    # os.remove(local_path)

    url = f"https://storage.googleapis.com/{bucket_name}/{bucket_path}"

    return JSONResponse({"task_id": task_id, "report_url": url, "message": "HR report generated"})


# =====================================================
# TECHNICAL REPORT
# =====================================================
@router.post("/technical")
def generate_technical_report(task_id: str = Form(...), db: Session = Depends(get_db)):
    responses = db.query(TechnicalRoundResponse).filter(TechnicalRoundResponse.task_id == task_id).all()
    if not responses:
        raise HTTPException(status_code=404, detail="No technical data found")

    qa_pairs = [
        {
            "question": r.question.question,
            "transcript": r.transcript,
            "correct_answer": r.question.answer
        }
        for r in responses
    ]

    report = generate_technical_report_with_gemini(qa_pairs)

    os.makedirs("Reports", exist_ok=True)
    local_path = f"Reports/{task_id}_technical.txt"
    with open(local_path, "w") as f:
        f.write(report)

    bucket_path = f"reports/{task_id}_technical.txt"
    upload_to_gcp_bucket(local_path, bucket_path)

    # OPTIONAL: delete local copy
    # os.remove(local_path)

    url = f"https://storage.googleapis.com/{bucket_name}/{bucket_path}"

    return JSONResponse({"task_id": task_id, "report_url": url, "message": "Technical report generated"})


# =====================================================
# CULTURAL REPORT
# =====================================================
@router.post("/cultural")
def generate_cultural_report(task_id: str = Form(...), db: Session = Depends(get_db)):
    responses = db.query(CulturalRoundResponse).filter(CulturalRoundResponse.task_id == task_id).all()
    if not responses:
        raise HTTPException(status_code=404, detail="No cultural data found")

    qa_pairs = [
        {"question": r.question.question_text, "transcript": r.transcript}
        for r in responses
    ]

    report = generate_cultural_report_with_gemini(qa_pairs)

    os.makedirs("Reports", exist_ok=True)
    local_path = f"Reports/{task_id}_cultural.txt"
    with open(local_path, "w") as f:
        f.write(report)

    bucket_path = f"reports/{task_id}_cultural.txt"
    upload_to_gcp_bucket(local_path, bucket_path)

    # OPTIONAL: delete local copy
    # os.remove(local_path)

    url = f"https://storage.googleapis.com/{bucket_name}/{bucket_path}"

    return JSONResponse({"task_id": task_id, "report_url": url, "message": "Cultural report generated"})


# ------------ GET HR REPORT ------------
@router.get("/hr/{task_id}")
def get_hr_report(task_id: str):
    bucket_path = f"reports/{task_id}_hr.txt"

    try:
        text = read_text_from_gcp_bucket(bucket_path)
        url = f"https://storage.googleapis.com/{bucket_name}/{bucket_path}"

        return {"task_id": task_id, "report_url": url, "content": text}

    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="HR report not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ------------ GET TECHNICAL REPORT ------------
@router.get("/technical/{task_id}")
def get_tech_report(task_id: str):
    bucket_path = f"reports/{task_id}_technical.txt"

    try:
        text = read_text_from_gcp_bucket(bucket_path)
        url = f"https://storage.googleapis.com/{bucket_name}/{bucket_path}"

        return {"task_id": task_id, "report_url": url, "content": text}

    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Technical report not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ------------ GET CULTURAL REPORT ------------
@router.get("/cultural/{task_id}")
def get_cultural_report(task_id: str):
    bucket_path = f"reports/{task_id}_cultural.txt"

    try:
        text = read_text_from_gcp_bucket(bucket_path)
        url = f"https://storage.googleapis.com/{bucket_name}/{bucket_path}"

        return {"task_id": task_id, "report_url": url, "content": text}

    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Cultural report not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
