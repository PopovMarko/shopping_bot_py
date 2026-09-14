import os
from functools import lru_cache

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    async_sessionmaker,
    create_async_engine,
)

load_dotenv()


@lru_cache(maxsize=1)
def get_engine() -> AsyncEngine:
    database_url = str(os.getenv("DATABASE_URL"))
    return create_async_engine(database_url, echo=False)


def async_session_factory():
    async_session_maker = async_sessionmaker(bind=get_engine(), expire_on_commit=False)
    return async_session_maker()
