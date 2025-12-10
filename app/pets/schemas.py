from pydantic import BaseModel
from typing import Optional
from datetime import date, time
from enum import Enum


class PetStatus(str, Enum):
    lost = "lost"
    found = "found"
    returned = "returned"
    closed = "closed"


class SPetBase(BaseModel):
    type: str
    breed: Optional[str] = None
    name: Optional[str] = None
    color: str
    sex: str
    age: Optional[str] = None

    chip_number: Optional[str] = None
    brand_number: Optional[str] = None

    found_date: date
    found_time: time
    address: str

    description: str
    status: PetStatus = PetStatus.lost


class SPetCreate(SPetBase):
    pass


class SPetUpdate(BaseModel):
    type: Optional[str] = None
    breed: Optional[str] = None
    name: Optional[str] = None
    color: Optional[str] = None
    sex: Optional[str] = None
    age: Optional[str] = None

    chip_number: Optional[str] = None
    brand_number: Optional[str] = None

    found_date: Optional[date] = None
    found_time: Optional[time] = None
    address: Optional[str] = None

    description: Optional[str] = None
    status: Optional[PetStatus] = None

    photo_url: Optional[str] = None


class SPetResponse(SPetBase):
    id: int
    owner_id: int
    photo_url: Optional[str] = None

    class Config:
        from_attributes = True
