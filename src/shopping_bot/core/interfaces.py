from typing import Protocol

from shopping_bot.core.domain import RequestUserDomain, ResponseUserDomain


class UserController(Protocol):
    async def start_cmd(self, user: RequestUserDomain) -> ResponseUserDomain: ...
