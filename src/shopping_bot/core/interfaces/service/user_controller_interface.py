from typing import Protocol

from shopping_bot.core.domains.user_domain import InputUserDomain, ResultUserDomain


class UserControllerInterface(Protocol):
    async def start_cmd(self, user: InputUserDomain) -> ResultUserDomain: ...
    async def get_user_id_by_telegram_id(self, user_telegram_id: int) -> int | None: ...
