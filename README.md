🎥 AI Video Interview Platform

An AI-powered automated interview evaluation system built using FastAPI, Python, and PostgreSQL.
The platform analyzes interview videos and generates detailed HR, Technical, and Cultural Fit assessments using LLMs and Google Vertex AI.

Project Structure

/Backend: FastAPI backend, APIs, model scoring, reports, and database logic

/Backend/routers: All API routes (HR, Technical, Cultural Fit, Upload, Users, Reports, Tasks)

/Backend/services: Background logic & processing utilities

/Backend/uploads: Temporary video & file storage

/Backend/key: GCP Vertex AI service account key

/Backend/Reports: Auto-generated interview reports

/frontend: Web interface (HTML/JS/React based)

database.sql: PostgreSQL schema

requirements.txt: Backend dependencies

.env: Environment configuration (DB URL, GCP key path)

Getting Started
Prerequisites

Python 3.9+

PostgreSQL

Node.js (if using frontend)

Google Cloud Vertex AI API Key (JSON)

Installation
1. Clone the Repository
git clone <repository-url>
cd AI_VIDEO_INTERVIEW

2. Backend Setup
cd Backend
python -m venv myenv
source myenv/bin/activate     # Windows: myenv\Scripts\activate
pip install -r requirements.txt


Create a .env file:

DATABASE_URL=postgresql://<user>:<password>@localhost:5432/ai_interview
GCP_KEY_PATH=key/vertex_api.json
BUCKET_NAME=<your-gcp-bucket>


Run the database schema:

psql -U postgres -d ai_interview -f database.sql

3. Frontend Setup (optional)
cd frontend
npm install
npm start

Running the Application
Start Backend
cd Backend
uvicorn main:app --reload


Visit:

Swagger Docs → http://localhost:8000/docs

ReDoc → http://localhost:8000/redoc

Start Frontend (if applicable)
npm start


Open browser → http://localhost:3000

Features

Video upload & processing

AI-driven interview scoring (HR, Technical, Cultural Fit)

Automatic transcript extraction

Confidence-level scoring

GCP Vertex AI integration

Task creation & tracking

Report generation (TXT/PDF)

User management endpoints