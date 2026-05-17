from sqlalchemy import create_engine, Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# This creates/connects to a file called tickets.db in your backend folder
DATABASE_URL = "sqlite:///./tickets.db"

# Engine = the connection to database
engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False}
)

# SessionLocal = how we talk to the database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base = parent class for all our database models
Base = declarative_base()

# This is our Ticket table definition
class TicketDB(Base):
    __tablename__ = "tickets"

    ticket_id   = Column(String, primary_key=True, index=True)
    title       = Column(String, nullable=False)
    description = Column(String, nullable=False)
    submitted_by = Column(String, nullable=False)
    status      = Column(String, default="open")
    ai_summary  = Column(String)
    ai_category = Column(String)
    ai_priority = Column(String)
    created_at  = Column(String)

# This creates the actual table in tickets.db
def init_db():
    Base.metadata.create_all(bind=engine)

# This gives us a database session to use in our API
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()