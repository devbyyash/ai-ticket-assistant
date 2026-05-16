from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
import uuid

# Create the FastAPI app
app = FastAPI(
    title="AI Ticket Assistant API",
    description="Enterprise Ticket Management powered by AI",
    version="1.0.0"
)

# Define what a Ticket looks like
class Ticket(BaseModel):
    title: str
    description: str
    submitted_by: str

# Define what the Response looks like
class TicketResponse(BaseModel):
    ticket_id: str
    title: str
    description: str
    submitted_by: str
    status: str
    created_at: str
    message: str

# Root endpoint - just to check if API is alive
@app.get("/")
def root():
    return {"message": "AI Ticket Assistant API is running 🚀"}

# Health check endpoint
@app.get("/health")
def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

# Submit a ticket endpoint
@app.post("/tickets", response_model=TicketResponse)
def submit_ticket(ticket: Ticket):
    
    # Generate a unique ticket ID
    ticket_id = f"TKT-{str(uuid.uuid4())[:8].upper()}"
    
    # Get current timestamp
    created_at = datetime.now().isoformat()
    
    # Build the response
    response = TicketResponse(
        ticket_id=ticket_id,
        title=ticket.title,
        description=ticket.description,
        submitted_by=ticket.submitted_by,
        status="open",
        created_at=created_at,
        message=f"Ticket {ticket_id} submitted successfully!"
    )
    
    return response