from sqlalchemy import (
    Column, Integer, String, Text, ForeignKey, DateTime, func
)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

# ============================================================
# USERS TABLE
# ============================================================
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    skill = Column(String(255), nullable=True)
    job_role = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # relationships
    #tasks = relationship("UserTask", back_populates="user", cascade="all, delete")
    # hr_responses = relationship("HrRoundResponse", back_populates="user")
    # tech_responses = relationship("TechnicalRoundResponse", back_populates="user")
    # cultural_responses = relationship("CulturalRoundResponse", back_populates="user")


# ============================================================
# USER TASKS TABLE
# ============================================================
# class UserTask(Base):
#     __tablename__ = "user_tasks"

#     id = Column(Integer, primary_key=True, index=True)
#     u_id = Column(String, nullable=False)
#     type = Column(String, nullable=False)
#     task_id = Column(String, nullable=False)

class UserTask(Base):
    __tablename__ = "user_tasks"

    id = Column(Integer, primary_key=True, index=True)
    u_id = Column(String, nullable=False)
    type = Column(String, nullable=False)
    task_id = Column(String, nullable=False)

    hr_responses = relationship("HrRoundResponse", back_populates="user_task")
    tech_responses = relationship("TechnicalRoundResponse", back_populates="user_task")
    cultural_responses = relationship("CulturalRoundResponse", back_populates="user_task")
# ============================================================
# TECHNICAL ROUND QUESTIONS
# ============================================================
class TechnicalRound(Base):
    __tablename__ = "technical_round"

    id = Column(Integer, primary_key=True, autoincrement=True)
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=True)
    skill = Column(String(255), nullable=True)
    difficulty = Column(String(50), nullable=True)

    responses = relationship("TechnicalRoundResponse", back_populates="question")


# ============================================================
# HR ROUND QUESTIONS
# ============================================================
class HrRound(Base):
    __tablename__ = "hr_round"

    id = Column(Integer, primary_key=True, autoincrement=True)
    question_text = Column(Text, nullable=False)

    responses = relationship("HrRoundResponse", back_populates="question")


# ============================================================
# CULTURAL FIT QUESTIONS
# ============================================================
class CulturalFit(Base):
    __tablename__ = "cultural_fit"

    id = Column(Integer, primary_key=True, autoincrement=True)
    question_text = Column(Text, nullable=False)

    responses = relationship("CulturalRoundResponse", back_populates="question")


# ============================================================
# TECHNICAL ROUND RESPONSES
# ============================================================
class TechnicalRoundResponse(Base):
    __tablename__ = "technical_round_response"

    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(String, ForeignKey("user_tasks.task_id", ondelete="CASCADE"), nullable=False)
    question_id = Column(Integer, ForeignKey("technical_round.id"), nullable=False)
    transcript = Column(Text, nullable=False)
    skill = Column(Text, nullable=False)

    user_task = relationship("UserTask", back_populates="tech_responses")
    question = relationship("TechnicalRound", back_populates="responses")


# ============================================================
# HR ROUND RESPONSES
# ============================================================
class HrRoundResponse(Base):
    __tablename__ = "hr_round_response"

    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(String, ForeignKey("user_tasks.task_id", ondelete="CASCADE"), nullable=False)
    question_id = Column(Integer, ForeignKey("hr_round.id"), nullable=False)
    transcript = Column(Text, nullable=False)

    user_task = relationship("UserTask", back_populates="hr_responses")
    question = relationship("HrRound", back_populates="responses")


# ============================================================
# CULTURAL ROUND RESPONSES
# ============================================================
class CulturalRoundResponse(Base):
    __tablename__ = "cultural_round_response"

    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(String, ForeignKey("user_tasks.task_id", ondelete="CASCADE"), nullable=False)
    question_id = Column(Integer, ForeignKey("cultural_fit.id"), nullable=False)
    transcript = Column(Text, nullable=False)

    user_task = relationship("UserTask", back_populates="cultural_responses")
    question = relationship("CulturalFit", back_populates="responses")
