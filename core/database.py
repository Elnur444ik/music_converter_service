from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, DeclarativeMeta, sessionmaker
from typing_extensions import AsyncGenerator

from core import settings

Base: DeclarativeMeta = declarative_base()

engine = create_async_engine(
    settings.DATABASE_URL,
    future=True,
    echo=True,
    execution_options={'isolation_level': 'AUTOCOMMIT'},
)

async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """Dependency for getting async session"""
    async with async_session_maker() as session:
        yield session
