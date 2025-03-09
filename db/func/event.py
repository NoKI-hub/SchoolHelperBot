from sqlalchemy import select
from sqlalchemy.orm import selectinload

from db.core.engine import AsyncSession
from db import models
from db.models import Event

from typing import Dict, Sequence, Any


async def all(
        filters: Dict[str, Any], 
        load: Sequence[Any], 
        std_load: bool = False
    ) -> Sequence[Event]:
    async with AsyncSession() as session:
        std_loads = [models.Event.users, models.Event.organizator, models.Event.type]
        if std_load:
            if load:
                load.extend(std_loads)
            else:
                load = std_loads
        stmt = select(models.Event).filter_by(**filters).options(selectinload(*load))
        result = await session.scalars(stmt)
        return result.all()


async def add(event: Event) -> None:
    async with AsyncSession() as session:
        session.add(event)
        await session.commit()
    

async def delete(event: Event) -> None:
    async with AsyncSession() as session:
        session.delete(event)
        await session.commit()
