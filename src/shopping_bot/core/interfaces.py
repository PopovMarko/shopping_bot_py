from typing import Protocol

from shopping_bot.core.domain import (
    RequestUserDomain,
    ResponseProductDomain,
    ResponseUserDomain,
)
from shopping_bot.core.repository_dto import UserRecord


class UserController(Protocol):
    async def start_cmd(self, user: RequestUserDomain) -> ResponseUserDomain: ...


class ProductController(Protocol):
    # async def find_product_by_name(self, product_name: str) -> tuple[str, bool]: ...
    async def process_quantity(
        self, product_id: str, quantity: str
    ) -> ResponseProductDomain: ...

    async def process_product(self, naem: str) -> ResponseProductDomain: ...
    async def process_confirmation(
        self, confirm: bool, product_id: int | None
    ) -> ResponseProductDomain: ...


class RepositoryController(Protocol):
    async def get_user_by_telegram_id(
        self, user_telegram_id: int
    ) -> UserRecord | None: ...

    async def save_user(self, user: RequestUserDomain) -> UserRecord: ...
