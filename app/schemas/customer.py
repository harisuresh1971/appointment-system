from pydantic import BaseModel
from datetime import datetime


class CustomerCreate(BaseModel):
    name: str
    phone: str


class CustomerUpdate(BaseModel):
    name: str | None = None
    phone: str | None = None


class CustomerResponse(BaseModel):
    id: int
    name: str
    phone: str
    created_at: datetime

    class Config:
        from_attributes = True
