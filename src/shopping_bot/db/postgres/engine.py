import os

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    async_sessionmaker,
    create_async_engine,
)


def async_session_factory():

    load_dotenv()

    DATABASE_URL = str(os.getenv("DATABASE_URL"))

    engine: AsyncEngine = create_async_engine(DATABASE_URL, echo=False)

    async_session_ = async_sessionmaker(bind=engine, expire_on_commit=False)

    return async_session_()
