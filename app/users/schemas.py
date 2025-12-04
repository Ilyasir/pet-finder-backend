from pydantic import BaseModel, EmailStr
from datetime import datetime

class SUserBase(BaseModel):
    email: EmailStr

class SUserCreate(SUserBase):
    password: str

class SUserResponse(SUserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
