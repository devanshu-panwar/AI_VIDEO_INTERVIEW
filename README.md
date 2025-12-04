# 🎥 AI Video Interview Platform

An AI-powered automatic video interview evaluation system built using **FastAPI**, **Python**, **PostgreSQL**, **Google Vertex AI**, and **LLMs**.  
The platform analyzes candidate interview videos, transcribes responses, and generates **Technical**, **HR**, and **Cultural Fit** assessments automatically.

---

## 📌 Features

- 🎬 Video upload & automated audio extraction  
- 🔊 Speech-to-text transcription (Google Vertex AI)  
- 🤖 AI-driven scoring for HR, Technical, and Cultural rounds  
- 🧠 LLM-powered report generation  
- 📄 Downloadable TXT/PDF reports  
- 🗃️ Task tracking & session management  
- 🧩 Modular, scalable FastAPI architecture  
- ☁️ GCP Cloud Storage integration  

---

## 📁 Project Structure

```
AI_Video_Interview/
│
├── Backend/                 
│   ├── routers/             # All API routes
│   ├── services/            # Core logic (audio, GCP, scoring, etc.)
│   ├── uploads/             # Temporary video/audio storage
│   ├── Reports/             # Generated TXT/PDF reports
│   ├── key/                 # Vertex AI service account key
│   ├── database.py          # DB setup
│   ├── models.py            # SQLAlchemy models
│   ├── schemas.py           # Pydantic schemas
│   ├── main.py              # FastAPI entry point
│   └── requirements.txt
│
├── frontend/                # Web interface (React / HTML / JS)
├── database.sql             # PostgreSQL schema
├── .env                     # Environment variables
└── README.md                # Documentation
```

---

## 🚀 Getting Started

### 1️⃣ Clone the Repository
```bash
git clone <repository-url>
cd AI_Video_Interview
```

---

## 🛠️ Backend Setup

```bash
cd Backend
python -m venv myenv
myenv\Scripts\activate  # Windows
# OR
source myenv/bin/activate # Mac/Linux

pip install -r requirements.txt
```

### Create `.env` file:

```
DATABASE_URL=postgresql://<user>:<password>@localhost:5432/ai_interview
GCP_KEY_PATH=key/vertex_api.json
BUCKET_NAME=<your-gcp-bucket>
```

### Run database schema:
```bash
psql -U postgres -d ai_interview -f database.sql
```

---

## 🌐 Running the Backend

```bash
uvicorn main:app --reload
```

Visit:

- Swagger → http://localhost:8000/docs  
- ReDoc → http://localhost:8000/redoc  

---

## 💻 Frontend Setup (Optional)

```bash
cd frontend
npm install
npm start
```

Open → http://localhost:3000

---

## 📡 API Endpoints

### Transcription
```
POST /transcribe
```

### Fetch Technical Report
```
GET /technical/{task_id}
```

### Create Interview Task
```
POST /tasks/generate_task
```

### User Info
```
GET /users/user-info?u_id=<value>
```

---

## 🧩 Tech Stack

| Layer | Technologies |
|-------|--------------|
| Backend | FastAPI, SQLAlchemy, Pydantic |
| AI | Google Vertex AI, LLMs |
| Storage | PostgreSQL, GCP Cloud Storage |
| Frontend | React / HTML / JavaScript |

---

## 📝 Example cURL

```bash
curl -X GET "http://localhost:8000/technical/<TASK_ID>"
```

---

## 🤝 Contributing

Pull requests are welcome! Please maintain clean code and commit standards.

---

## 📜 License

This project is licensed under your selected license (MIT/GPL/Apache).
