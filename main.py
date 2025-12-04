from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from dotenv import load_dotenv
import vertexai
import os

from routers import users, hr_round, technical_round, cultural_fit, upload, reports, tasks

load_dotenv()

app = FastAPI(title="AI Video Interview System")

# ✅ CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Vertex AI initialization
gcp_project = os.getenv("GOOGLE_CLOUD_PROJECT")
gcp_region = os.getenv("GOOGLE_CLOUD_LOCATION")
vertexai.init(project=gcp_project, location=gcp_region)

# ✅ Routers
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(hr_round.router, prefix="/hr-round", tags=["HR Round"])
app.include_router(technical_round.router, prefix="/technical-round", tags=["Technical Round"])
app.include_router(cultural_fit.router, prefix="/cultural-fit", tags=["Cultural Fit"])
app.include_router(upload.router, prefix="/upload", tags=["Upload"])
app.include_router(reports.router, prefix="/reports", tags=["Reports"])
app.include_router(tasks.router, prefix="/tasks", tags=["Tasks"])


@app.get("/")
async def root():
    return {"message": "Backend API is running successfully 🚀"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
