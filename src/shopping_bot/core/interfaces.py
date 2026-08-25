from typing import Protocol

from shopping_bot.core.domain import RequestUserDomain, ResponseUserDomain
from shopping_bot.core.repository_dto import UserRecord


class UserController(Protocol):
    async def start_cmd(self, user: RequestUserDomain) -> ResponseUserDomain: ...


class RepositoryController(Protocol):
    async def get_user_by_telegram_id(
        self, user_telegram_id: int
    ) -> UserRecord | None: ...

    async def save_user(self, user: RequestUserDomain) -> UserRecord: ...
