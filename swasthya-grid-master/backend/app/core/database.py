from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base
from sqlalchemy import text
from app.core.config import settings

# Create Async SQLAlchemy Engine with 2-second connection timeout
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DB_ECHO,
    pool_size=settings.DB_POOL_SIZE,
    max_overflow=settings.DB_MAX_OVERFLOW,
    pool_pre_ping=True,
    connect_args={"timeout": 2.0}
)

# Create Async Session Factory
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
    class_=AsyncSession
)

# Declarative Base for SQLAlchemy Models
Base = declarative_base()


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    FastAPI dependency that yields an asynchronous database session.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def check_database_connection() -> dict:
    """
    Utility function to verify database connectivity with fast timeout.
    """
    try:
        async with AsyncSessionLocal() as session:
            result = await session.execute(text("SELECT 1 AS alive, current_database() AS db_name, version() AS pg_version;"))
            row = result.mappings().first()
            return {
                "connected": True,
                "database": row["db_name"],
                "version": row["pg_version"]
            }
    except Exception as e:
        return {
            "connected": False,
            "error": str(e)
        }
