import os

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    async_sessionmaker,
    create_async_engine,
)

load_dotenv()

DATABASE_URL = str(os.getenv("DATABASE_URL"))

engine: AsyncEngine = create_async_engine(DATABASE_URL, echo=True)

async_session_factory = async_sessionmaker(bind=engine, expire_on_commit=False)
