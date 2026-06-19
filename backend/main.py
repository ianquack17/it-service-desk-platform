from fastapi import FastAPI, HTTPException

app = FastAPI()

tickets = []
next_id = 1

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/tickets")
def get_tickets():
    return tickets 

@app.post("/tickets")
def create_ticket(ticket: dict):

    global next_id
    ticket["id"] = next_id
    next_id += 1

    tickets.append(ticket)

    return {
        "message": "Ticket created successfully", "ticket": ticket
    }

@app.get("/tickets/{ticket_id}")
def get_ticket(ticket_id: int):
    for ticket in tickets:
        if ticket.get("id") == ticket_id:
            return ticket
    raise HTTPException(status_code=404, detail="Ticket not found")

@app.delete("/tickets/{ticket_id}")
def delete_ticket(ticket_id: int):
    for ticket in tickets:
        if ticket.get("id") == ticket_id:
            tickets.remove(ticket)
            return {"message": "Ticket deleted successfully"}
    raise HTTPException(status_code=404, detail="Ticket not found")

@app.patch("/tickets/{ticket_id}")
def update_ticket(ticket_id: int, updated_ticket: dict):
    for ticket in tickets:
        if ticket.get("id") == ticket_id:
            ticket.update(updated_ticket)
            return {"message": "Ticket updated successfully", "ticket": ticket}
    raise HTTPException(status_code=404, detail="Ticket not found")
