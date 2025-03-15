from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from config.config import settings


engine = create_async_engine(
    settings.DB_URL if not settings.DEBUG else settings.DEBUG_DB_URL,
    echo=False,
)

AsyncSession = async_sessionmaker(engine, expire_on_commit=False)
