from pydantic import BaseModel, Field

class TicketCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1)
    status: str = "Open"
    priority: str = "Low"

class TicketUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    status: str | None = None
    priority: str | None = None