from fastapi import APIRouter, File, UploadFile, Form, HTTPException, Depends
from services.audio_processing import extract_audio_from_compressed_video, transcribe_with_vertex_ai
from services.gcp_helper import upload_to_gcp_bucket, bucket_name
from database import get_db
import os, shutil, uuid, logging
from models import HrRoundResponse, TechnicalRoundResponse, CulturalRoundResponse
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/transcribe")
async def process_audio_for_transcription(
    video_file: UploadFile = File(...),
    task_id: str = Form(...),
    question_id: int = Form(...),
    round_type: str = Form(...),
    skill: str = Form(None),   # Only used for TECHNICAL
    db: Session = Depends(get_db)
):
    try:
        os.makedirs("uploads", exist_ok=True)

        base = f"{task_id}_{uuid.uuid4().hex[:6]}"
        video_path = f"uploads/{base}.webm"
        audio_path = f"uploads/{base}.wav"

        # Save uploaded video
        with open(video_path, "wb") as f:
            shutil.copyfileobj(video_file.file, f)

        # Extract audio
        extract_audio_from_compressed_video(video_path, audio_path)

        # Upload audio to GCP
        gcp_audio_path = f"audios/{base}.wav"
        upload_to_gcp_bucket(audio_path, gcp_audio_path)

        # Transcribe with Vertex
        gcs_uri = f"gs://{bucket_name}/{gcp_audio_path}"
        transcript = transcribe_with_vertex_ai(gcs_uri)

        # -----------------------------
        # Insert into correct response table
        # -----------------------------
        round_type_lower = round_type.lower()

        if round_type_lower == "technical":
            record = TechnicalRoundResponse(
                task_id=task_id,
                question_id=question_id,
                transcript=transcript,
                skill=skill  # ONLY technical has skill
            )

        elif round_type_lower == "hr":
            record = HrRoundResponse(
                task_id=task_id,
                question_id=question_id,
                transcript=transcript
            )

        elif round_type_lower == "cultural":
            record = CulturalRoundResponse(
                task_id=task_id,
                question_id=question_id,
                transcript=transcript
            )

        else:
            raise HTTPException(status_code=400, detail="Invalid round type")

        db.add(record)
        db.commit()
        db.refresh(record)

        # Cleanup temp files
        os.remove(video_path)
        os.remove(audio_path)

        return {
            "message": "Processed successfully",
            "transcript": transcript,
            "audio_url": gcs_uri
        }

    except Exception as e:
        logging.error(f"Transcription failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))
