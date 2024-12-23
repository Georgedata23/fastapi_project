from sqlalchemy.dialects.postgresql.psycopg import logger
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from app.config import settings


engine = create_async_engine(settings.DATABASE_URL)
async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def get_session() -> AsyncSession:
    async with async_session_maker() as session:
        logger.info("Отрабатывает get_session!")
        yield session

class Base(DeclarativeBase):
    pass