🎥 AI Video Interview Platform

A fully automated AI-powered video interview assessment system built using FastAPI, Python, PostgreSQL, Google Vertex AI, and LLMs.
The platform evaluates candidates across Technical, HR, and Cultural Fit rounds using video analysis, transcription, scoring, and report generation.

📁 Project Structure
AI_Video_Interview
│
├── Backend/                    # FastAPI backend
│   ├── routers/                # All API routes (HR, Technical, Cultural, Users, Tasks, Reports)
│   ├── services/               # Audio processing, GCP helpers, scoring logic, LLM operations
│   ├── uploads/                # Temporary video/audio storage
│   ├── Reports/                # Auto-generated reports (TXT/PDF)
│   ├── key/                    # Vertex AI service account key
│   ├── database.py             # DB connection + Base models
│   ├── models.py               # SQLAlchemy ORM models
│   ├── schemas.py              # Pydantic schemas
│   ├── main.py                 # FastAPI entry point
│   └── requirements.txt        # Backend dependencies
│
├── frontend/                   # Web interface (React / HTML / JS)
│
├── database.sql                # PostgreSQL schema
├── .env                        # Environment variables
└── README.md                   # Project documentation

🚀 Getting Started
✅ Prerequisites

Python 3.9+

PostgreSQL

Node.js + npm (if running frontend)

Google Cloud Vertex AI Key (JSON)

🛠️ Installation
1. Clone the Repository
git clone <repository-url>
cd AI_Video_Interview

2. Backend Setup
cd Backend
python -m venv myenv
# Windows:
myenv\Scripts\activate
# Mac/Linux:
source myenv/bin/activate
pip install -r requirements.txt

Create your .env:
DATABASE_URL=postgresql://<user>:<password>@localhost:5432/ai_interview
GCP_KEY_PATH=key/vertex_api.json
BUCKET_NAME=<your-gcp-bucket>

Initialize PostgreSQL:
psql -U postgres -d ai_interview -f database.sql

3. Frontend Setup (Optional)
cd frontend
npm install
npm start

▶️ Running the Application
Start Backend
cd Backend
uvicorn main:app --reload


Open:

Swagger API Docs → http://localhost:8000/docs

ReDoc → http://localhost:8000/redoc

Start Frontend
npm start


Open browser → http://localhost:3000

🌟 Features
🎬 Video Upload & Audio Extraction

Extracts audio from uploaded .webm video files

Converts and stores them in GCP buckets

🧠 AI-Driven Interview Scoring

Uses Google Vertex AI + LLMs

Generates scoring for:
✔ Technical Round
✔ HR Round
✔ Cultural Fit Round

📝 Auto-Generated Reports

TXT/PDF report generation

Detailed scoring + feedback

Downloadable URLs

🔊 Transcription Pipeline

Converts candidate speech to text

Ultra-fast processing

Supports noisy audio handling

🧩 Modular Architecture

Clean separation of routers

Extensible scoring logic

Scalable design for large interviews

🗃️ Database + Task Tracking

PostgreSQL relational schema

Auto-generated task IDs

Tracks user interviews & responses

📡 API Highlights
📤 Upload + Transcribe Video
POST /transcribe

📄 Fetch Technical Report
GET /technical/{task_id}

⚙️ Generate Interview Task
POST /tasks/generate_task

👤 User Management
POST /users/create
GET /users/user-info

📄 Example cURL
curl -X GET "http://localhost:8000/technical/<TASK_ID>"

🧪 Tech Stack
Backend

FastAPI

Python 3.9+

SQLAlchemy ORM

Pydantic v2

AI/ML

Google Vertex AI

LLM-based scoring

Speech-to-Text transcription

Storage

Google Cloud Storage

PostgreSQL

Frontend

React / HTML / JavaScript

📜 License

This project is licensed under your chosen license (MIT/GPL/Apache).
Add a LICENSE file to specify.

🤝 Contributing

Pull requests are welcome!
Make sure to follow structured commits and formatting.
