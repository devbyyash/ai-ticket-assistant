# 🎫 AI-Powered Enterprise Ticket Assistant

An intelligent ticket management system built with Python, FastAPI, and AI.

## 🚀 Features
- Submit support tickets via web UI
- AI automatically analyzes each ticket using LLaMA 3.3 70B
- Auto-categorization (SAP-ERP, Network, Finance, HR, etc.)
- Auto-priority detection (Low / Medium / High / Critical)
- AI-generated one-line summary
- Persistent storage with SQLite database
- Live dashboard with filters and stats

## 🛠️ Tech Stack
| Layer | Technology |
|---|---|
| Backend | Python, FastAPI |
| AI Engine | Groq API + LLaMA 3.3 70B |
| Database | SQLite + SQLAlchemy |
| Frontend | HTML, CSS, JavaScript |
| Deployment | SAP BTP (coming soon) |

## 📦 Setup Instructions

### 1. Clone the repo
git clone https://github.com/devbyyash/ai-ticket-assistant.git
cd ai-ticket-assistant

### 2. Setup backend
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

### 3. Add your API key
Create backend/.env file:
GROQ_API_KEY=your_groq_api_key_here

### 4. Run the backend
uvicorn main:app --reload

### 5. Open frontend
Open frontend/index.html in your browser

## 📸 Screenshots
### Ticket Submission
Submit tickets and get instant AI analysis

### Dashboard
View all tickets with real-time stats and filters

## 🔗 API Endpoints
| Method | Endpoint | Description |
|---|---|---|
| GET | / | Health check |
| GET | /health | Detailed health |
| POST | /tickets | Submit new ticket |
| GET | /tickets | Get all tickets |

## 👨‍💻 Built By
Yash — SAP BTP + AI Developer