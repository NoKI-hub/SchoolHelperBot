from sqlalchemy import select
from sqlalchemy.orm import selectinload

from db.core.engine import AsyncSession
from db.models import User


async def add(user: User):
    async with AsyncSession() as session:
        session.add(user)
        await session.commit()


async def by_id(id: int, *load):
    async with AsyncSession() as session:
        stmt = select(User).filter_by(id=id)
        if load: stmt = stmt.options(selectinload(*load))
        return await session.scalar(stmt)
    

async def update(user: User):
    async with AsyncSession() as session:
        session.add(user)
        await session.commit()
    