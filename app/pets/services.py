from app.database import async_session
from app.pets.models import Pet
from sqlalchemy.future import select

from app.base import BaseService


class PetService(BaseService):
    model = Pet

    @classmethod
    async def create_pet(cls, pet_data: dict):
        async with async_session() as session:
            new_pet = Pet(**pet_data)
            session.add(new_pet)
            await session.commit()
            await session.refresh(new_pet)
            return new_pet

    @classmethod
    async def update_pet(cls, pet_id: int, pet_data: dict):
        async with async_session() as session:
            result = await session.execute(select(Pet).where(Pet.id == pet_id))
            pet = result.scalar_one_or_none()

            if not pet:
                return None

            for key, value in pet_data.items():
                setattr(pet, key, value)

            await session.commit()
            await session.refresh(pet)

            return pet

    @classmethod
    async def delete_pet(cls, pet_id: int):
        async with async_session() as session:
            result = await session.execute(select(Pet).where(Pet.id == pet_id))
            pet = result.scalar_one_or_none()

            if not pet:
                return False

            await session.delete(pet)
            await session.commit()
            return True
