import numpy as np

from app.database import async_session
from app.pets.models import Pet
from sqlalchemy.future import select

from app.base import BaseService
from app.pets.schemas import SPetResponse

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
        
    @classmethod
    async def find_similar_by_embedding(cls, pet_type: str, emb: list[float], top_k: int = 5):
        emb_np = np.array(emb, dtype=np.float32)

        async with async_session() as session:
            q = select(Pet).where(
                Pet.type == pet_type,
                Pet.embedding.isnot(None)
            )
            res = await session.execute(q)
            pets = res.scalars().all()

        if not pets:
            return []

        scored = []
        for pet in pets:
            vec = np.array(pet.embedding, dtype=np.float32)
            score = float(np.dot(emb_np, vec))

            scored.append({
                "pet": SPetResponse.from_orm(pet),
                "score": score
            })

        scored.sort(key=lambda x: x["score"], reverse=True)
        return scored[:top_k]
