from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy import Enum as SqlEnum
from sqlalchemy.sql import func
from database import Base

class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100))
    description = Column(Text)
    status = Column(SqlEnum("Open", "In Progress", "Closed", "Waiting for Reply", "On Hold", name="ticket_status"))
    priority = Column(SqlEnum("Low", "Medium", "High", "Urgent", name="ticket_priority"))
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=True)