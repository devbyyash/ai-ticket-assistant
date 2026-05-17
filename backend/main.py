from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
import uuid
from groq import Groq
import os
from dotenv import load_dotenv
from sqlalchemy.orm import Session
from database import TicketDB, get_db, init_db

# Load environment variables
load_dotenv()

# Configure Groq AI client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Create the FastAPI app
app = FastAPI(
    title="AI Ticket Assistant API",
    description="Enterprise Ticket Management powered by AI",
    version="3.0.0"
)

# Allow frontend to talk to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create database tables on startup
@app.on_event("startup")
def startup_event():
    init_db()
    print("✅ Database initialized!")

# ─── Models ───────────────────────────────────────────

class Ticket(BaseModel):
    title: str
    description: str
    submitted_by: str

class TicketResponse(BaseModel):
    ticket_id: str
    title: str
    description: str
    submitted_by: str
    status: str
    created_at: str
    ai_summary: str
    ai_category: str
    ai_priority: str
    message: str

# ─── Endpoints ────────────────────────────────────────

@app.get("/")
def root():
    return {"message": "AI Ticket Assistant API is running 🚀"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

# ─── AI Analysis ──────────────────────────────────────

def analyze_ticket_with_ai(title: str, description: str) -> dict:

    prompt = f"""
    You are an enterprise IT support AI assistant.
    Analyze the following support ticket and respond ONLY in this exact format:

    SUMMARY: <one line summary of the issue>
    CATEGORY: <one of: Authentication, Network, Finance, HR, Infrastructure, SAP-ERP, Access-Management, Other>
    PRIORITY: <one of: Low, Medium, High, Critical>

    Ticket Title: {title}
    Ticket Description: {description}

    Rules:
    - SUMMARY must be under 20 words
    - CATEGORY must be exactly one from the list
    - PRIORITY must be exactly one from the list
    - No extra text, no explanation
    """

    chat_completion = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama-3.3-70b-versatile",
    )

    result_text = chat_completion.choices[0].message.content.strip()

    lines = result_text.split("\n")
    ai_data = {}

    for line in lines:
        if line.startswith("SUMMARY:"):
            ai_data["summary"] = line.replace("SUMMARY:", "").strip()
        elif line.startswith("CATEGORY:"):
            ai_data["category"] = line.replace("CATEGORY:", "").strip()
        elif line.startswith("PRIORITY:"):
            ai_data["priority"] = line.replace("PRIORITY:", "").strip()

    ai_data.setdefault("summary", "Unable to generate summary")
    ai_data.setdefault("category", "Other")
    ai_data.setdefault("priority", "Medium")

    return ai_data

# ─── Submit Ticket ────────────────────────────────────

@app.post("/tickets", response_model=TicketResponse)
def submit_ticket(ticket: Ticket, db: Session = Depends(get_db)):

    # Generate unique ticket ID
    ticket_id = f"TKT-{str(uuid.uuid4())[:8].upper()}"
    created_at = datetime.now().isoformat()

    # AI analysis
    ai_result = analyze_ticket_with_ai(ticket.title, ticket.description)

    # Save to database ← NEW!
    db_ticket = TicketDB(
        ticket_id    = ticket_id,
        title        = ticket.title,
        description  = ticket.description,
        submitted_by = ticket.submitted_by,
        status       = "open",
        ai_summary   = ai_result["summary"],
        ai_category  = ai_result["category"],
        ai_priority  = ai_result["priority"],
        created_at   = created_at
    )
    db.add(db_ticket)
    db.commit()

    print(f"✅ Ticket {ticket_id} saved to database!")

    return TicketResponse(
        ticket_id    = ticket_id,
        title        = ticket.title,
        description  = ticket.description,
        submitted_by = ticket.submitted_by,
        status       = "open",
        created_at   = created_at,
        ai_summary   = ai_result["summary"],
        ai_category  = ai_result["category"],
        ai_priority  = ai_result["priority"],
        message      = f"Ticket {ticket_id} submitted and saved successfully!"
    )

# ─── Get All Tickets ──────────────────────────────────

@app.get("/tickets")
def get_all_tickets(db: Session = Depends(get_db)):
    tickets = db.query(TicketDB).order_by(TicketDB.created_at.desc()).all()
    return {
        "total": len(tickets),
        "tickets": tickets
    }