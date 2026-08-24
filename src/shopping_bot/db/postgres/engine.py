from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    async_sessionmaker,
    create_async_engine,
)

DATABASE_URL = "postgresql+asyncpg://user:password@localhost:5432/db_name"

engine: AsyncEngine = create_async_engine(DATABASE_URL, echo=True)

async_session_factory = async_sessionmaker(bind=engine, expire_on_commit=False)
