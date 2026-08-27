from typing import Protocol

from shopping_bot.core.domain import (
    ProductDomain,
    RequestDomain,
    RequestUserDomain,
    UserDomain,
)
from shopping_bot.core.repository_dto import ProductRecord, RequestRecord, UserRecord


class UserControllerInterface(Protocol):
    async def start_cmd(self, user: RequestUserDomain) -> UserDomain: ...


class ProductControllerInterface(Protocol):
    async def process_product(self, naem: str) -> ProductDomain: ...
    async def process_confirmation(
        self, confirmed: bool, product_id: int | None, product_name: str | None
    ) -> ProductDomain: ...


class RequestControllerInterface(Protocol):
    async def process_quantity(
        self, product_id: int, quantity: str
    ) -> RequestDomain: ...


class UserRepositoryInterface(Protocol):
    async def get_user_by_telegram_id(
        self, user_telegram_id: int
    ) -> UserRecord | None: ...

    async def save_user(self, user: RequestUserDomain) -> UserRecord: ...


class ProductRepositoryInterface(Protocol):
    async def get_products(self) -> list[ProductRecord]: ...
    async def get_product(self, id: int) -> ProductRecord: ...
    async def create_product(self, name: str) -> ProductRecord: ...


class RequestRepositoryInterface(Protocol):
    async def create_request(self, product_id: int, quantity: int) -> RequestRecord: ...
