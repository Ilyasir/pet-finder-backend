from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime
from enum import Enum

class PetStatus(str, Enum):
    lost = "lost"
    found = "found"
    returned = "returned"
    closed = "closed"

class SPetBase(BaseModel):
    type: str
    name: Optional[str] = None
    description: Optional[str] = None
    city: str
    last_seen: Optional[str] = None
    date_lost: Optional[date] = None
    photo_url: Optional[str] = None
    status: PetStatus = PetStatus.lost

class SPetCreate(SPetBase):
    owner_id: int

class SPetUpdate(BaseModel):
    type: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    city: Optional[str] = None
    last_seen: Optional[str] = None
    date_lost: Optional[date] = None
    photo_url: Optional[str] = None
    status: Optional[PetStatus] = None

class SPetResponse(SPetBase):
    id: int
    owner_id: int
    created_at: datetime

    class Config:
        from_attributes = True
