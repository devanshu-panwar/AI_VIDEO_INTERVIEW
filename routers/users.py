# routers/users.py
from fastapi import APIRouter, HTTPException
import httpx
from pydantic import BaseModel

router = APIRouter()

BASE_URL = "https://aitq-backend-api-455331522955.us-central1.run.app/api/auth"

class LoginRequest(BaseModel):
    email_address: str
    password: str

@router.post("/login")
async def login(payload: LoginRequest):
    async with httpx.AsyncClient(timeout=20) as client:
        resp = await client.post(f"{BASE_URL}/login", json=payload.dict())
    if resp.status_code != 200:
        raise HTTPException(status_code=resp.status_code, detail=resp.text)
    return resp.json()

@router.get("/user-info")
async def user_info(u_id: str):
    async with httpx.AsyncClient(timeout=20) as client:
        resp = await client.get(f"{BASE_URL}/user-info", params={"u_id": u_id})
    if resp.status_code != 200:
        raise HTTPException(status_code=resp.status_code, detail=resp.text)
    return resp.json()

