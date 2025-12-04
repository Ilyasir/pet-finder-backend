from app.database import async_session
from app.pets.models import Pet

from app.base import BaseService

class PetService(BaseService):
    model = Pet
        
    @classmethod
    async def create_pet(cls, pet_data):
        async with async_session() as session:
            new_pet = Pet(**pet_data)
            session.add(new_pet)
            await session.commit()
            await session.refresh(new_pet)
            return new_pet