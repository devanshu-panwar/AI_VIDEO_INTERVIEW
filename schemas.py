from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime


# ==========================
# User Schemas
# ==========================

class UserBase(BaseModel):
    name: str
    email: EmailStr
    skill: Optional[str] = None
    job_role: Optional[str] = None


class UserCreate(UserBase):
    pass


class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    skill: Optional[str] = None
    job_role: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class SubmitResponse(BaseModel):
    message: str
    data: UserResponse

# ----------- Task_id --------------
class UserTaskCreate(BaseModel):
    u_id: str
    type: str

# class UserTaskResponse(BaseModel):
#     id: int
#     user_id: int
#     type: str
#     task_id: str

#     class Config:
#         from_attributes = True

class UIDRequest(BaseModel):
    u_id: str


class UserTaskResponse(BaseModel):
    id: int
    u_id: str
    type: str
    task_id: str

    class Config:
        from_attributes = True

# ==========================
# Question Schemas
# ==========================
class HRQuestion(BaseModel):
    id: int
    question_text: str

    class Config:
        from_attributes = True


class TechnicalQuestion(BaseModel):
    id: int
    question: str
    answer: Optional[str]
    skill: Optional[str]
    difficulty: Optional[str]

    class Config:
        from_attributes = True


class CulturalQuestion(BaseModel):
    id: int
    question_text: str

    class Config:
        from_attributes = True


# ==========================
# Response Schemas
# ==========================
class HRResponse(BaseModel):
    task_id: str
    question_text: str
    transcript: str


class TechnicalResponse(BaseModel):
    task_id: str
    question: str
    transcript: str
    skill: str
    correct_answer: Optional[str] = None


class CulturalResponse(BaseModel):
    task_id: str
    question: str
    transcript: str


# ==========================
# Report Schemas
# ==========================
class ReportGenerateRequest(BaseModel):
    task_id: str


class ReportGenerateResponse(BaseModel):
    task_id: str
    report_url: str
    message: str
