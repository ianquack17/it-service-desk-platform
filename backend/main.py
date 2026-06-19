from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from database import SessionLocal
from schemas import TicketCreate, TicketUpdate
import models


app = FastAPI()
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/tickets")
def get_tickets(db: Session = Depends(get_db)):
    return db.query(models.Ticket).all()

@app.post("/tickets")
def create_ticket(ticket: TicketCreate, db: Session = Depends(get_db)):

    new_ticket_data = ticket.model_dump()
    new_ticket_data["category"] = categorize_ticket(
        new_ticket_data["title"],
        new_ticket_data["description"]
    )
    new_ticket = models.Ticket(**new_ticket_data)
    db.add(new_ticket)
    db.commit()
    db.refresh(new_ticket)

    return {
        "message": "Ticket created successfully",
        "ticket": new_ticket
    }

@app.get("/tickets/{ticket_id}")
def get_ticket(ticket_id: int, db: Session = Depends(get_db)):
    ticket = (
    db.query(models.Ticket)
    .filter(models.Ticket.id == ticket_id)
    .first()
    )

    if ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")
        
    return ticket

@app.delete("/tickets/{ticket_id}")
def delete_ticket(ticket_id: int, db: Session = Depends(get_db)):
    ticket = (
        db.query(models.Ticket)
        .filter(models.Ticket.id == ticket_id)
        .first()
    )

    if ticket is None:
        raise HTTPException(status_code=404, detail="Ticket not found")
    
    db.delete(ticket)
    db.commit()

    return {"message": "Ticket succesfully deleted"}

@app.patch("/tickets/{ticket_id}")
def update_ticket(ticket_id: int, updated_ticket: TicketUpdate, db: Session = Depends(get_db)):
    ticket = (
        db.query(models.Ticket)
        .filter(models.Ticket.id == ticket_id)
        .first()
    )

    if ticket is None: 
        raise HTTPException(status_code=404, detail="Ticket not found")
    
    updated_data = updated_ticket.model_dump(exclude_unset=True)
    
    if not updated_data:
        raise HTTPException(
            status_code=400,
            detail="No fields provided to update"
        )
    
    for key, value in updated_data.items():
        setattr(ticket, key, value)

    ticket.updated_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(ticket)

    return {"message": "Ticket successfully modified",
            "ticket": ticket}


# Helper Functions

def categorize_ticket(title: str, description: str):
    title = title.lower()
    description = description.lower()

    if "password" in title:
        return "Password & Login Issue"
    else:
        return "General Support"