from app.database import async_session
from sqlalchemy import insert, select

class BaseService:
    model = None

    @classmethod
    async def find_all(cls):
        async with async_session() as session:
            query = select(cls.model)
            result = await session.execute(query)
            return result.scalars().all()
        
    @classmethod
    async def find_by_id(cls, entity_id: int):
        async with async_session() as session:
            query = select(cls.model).where(cls.model.id == entity_id)
            result = await session.execute(query)
            return result.scalar_one_or_none()
        
    @classmethod
    async def find_one_or_none(cls, **filters):
        async with async_session() as session:
            query = select(cls.model).filter_by(**filters)
            result = await session.execute(query)
            return result.scalar_one_or_none()
        
    @classmethod
    async def add(cls, **data):
        async with async_session() as session:
            query = insert(cls.model).values(**data)
            await session.execute(query)
            await session.commit()