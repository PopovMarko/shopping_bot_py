from dataclasses import asdict

from sqlalchemy import insert, select

from shopping_bot.core.domain import RequestUserDomain
from shopping_bot.core.repository_dto import UserRecord
from shopping_bot.core.utils import user_model_to_record
from shopping_bot.db.models import UserModel
from shopping_bot.db.postgres.engine import async_session_factory


class UserRepository:
    async def get_user_by_telegram_id(self, user_telegram_id: int) -> UserRecord | None:
        async with async_session_factory() as session:
            res = await session.execute(
                select(UserModel).where(UserModel.telegram_id == user_telegram_id)
            )
            user_model = res.scalar_one_or_none()
            if user_model is None:
                return None
            return user_model_to_record(user_model)

    async def save_user(self, user: RequestUserDomain) -> UserRecord:
        async with async_session_factory() as session:
            result = await session.execute(
                insert(UserModel).values(**asdict(user)).returning(UserModel)
            )
            await session.commit()
            user_model = result.scalar_one()
            return user_model_to_record(user_model)
