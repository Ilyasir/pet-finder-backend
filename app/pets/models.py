from sqlalchemy import Column, Integer, String, Text, Date, Time, ForeignKey, Enum, Float
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ARRAY
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
    breed = Column(String(100), nullable=True)
    name = Column(String(255), nullable=True)
    color = Column(String(100), nullable=False)
    sex = Column(String(10), nullable=False)
    age = Column(String(50), nullable=True)
    chip_number = Column(String(100), nullable=True)
    brand_number = Column(String(100), nullable=True)

    found_date = Column(Date, nullable=False)
    found_time = Column(Time, nullable=False)
    address = Column(String(255), nullable=False)

    description = Column(Text, nullable=False)

    photo_url = Column(String(500), nullable=True)

    status = Column(Enum(PetStatus, name="pet_status"), nullable=False, default=PetStatus.lost)
    embedding = Column(ARRAY(Float), nullable=True)