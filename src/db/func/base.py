from db.core.engine import engine
from db.core.base import Base


async def create_tables(if_not_exist: bool = False):
    async with engine.connect() as conn:
        if not if_not_exist: await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        await conn.commit()
