from sqlalchemy import select, delete as sql_delete
from sqlalchemy.orm import selectinload

from db.core.engine import AsyncSession
from db import models
from db.models import Event

from typing import Dict, List, Sequence, Any


async def all(
        filters: Dict[str, Any] = dict(), 
        load: List[Any] = [], 
        std_load: bool = False
    ) -> Sequence[Event]:
    async with AsyncSession() as session:
        if std_load:
            std_loads = [models.Event.user, models.Event.organizator, models.Event.type]
            if load:
                load.extend(std_loads)
            else:
                load = std_loads
        stmt = select(models.Event)
        if filters:
            stmt = stmt.filter_by(**filters)
        if load or std_load:
            stmt = stmt.options(selectinload(*load))
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


async def delete_by_id(event_id: int) -> None:
    async with AsyncSession() as session:
        stmt = sql_delete(models.Event).filter_by(id=event_id)
        await session.execute(stmt)
        await session.commit()