from sqlalchemy import Column, Integer, String, Text, Date, TIMESTAMP, ForeignKey, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base
import enum

class PetStatus(enum.Enum):
    lost = "lost"
    found = "found"
    returned = "returned"
    closed = "closed"

class Pet(Base):
    __tablename__ = "pets"

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    owner = relationship("User", back_populates="pets")

    type = Column(String(50), nullable=False)
    name = Column(String(255), nullable=True)
    description = Column(Text, nullable=True)
    city = Column(String(255), nullable=False)
    last_seen = Column(Text, nullable=True)
    date_lost = Column(Date, nullable=True)
    photo_url = Column(String(255), nullable=True)

    status = Column(Enum(PetStatus, name="pet_status"), nullable=False, default=PetStatus.lost)

    created_at = Column(TIMESTAMP, server_default=func.now())
