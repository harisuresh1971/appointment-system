from pydantic import BaseModel
from datetime import date, time, datetime
from typing import Optional


class AppointmentCreate(BaseModel):
    customer_id: int
    date: date
    time: time
    notes: str = ""
    status: str = "Scheduled"


class AppointmentUpdate(BaseModel):
    date: Optional[date] = None
    time: Optional[time] = None
    notes: Optional[str] = None
    status: Optional[str] = None


class AppointmentResponse(BaseModel):
    id: int
    customer_id: int
    date: date
    time: time
    notes: str
    status: str
    created_at: datetime

    class Config:
        from_attributes = True
