from typing import Protocol

from shopping_bot.core.domains.user_domain import InputUserDomain
from shopping_bot.core.records.user_records import ResponseUserRecord


class UserRepositoryInterface(Protocol):
    async def get_user_by_telegram_id(
        self, user_telegram_id: int
    ) -> ResponseUserRecord | None: ...

    async def save_user(self, user: InputUserDomain) -> ResponseUserRecord: ...
