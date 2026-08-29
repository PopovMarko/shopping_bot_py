from typing import Protocol

from shopping_bot.core.domains.product_domain import (
    InputProductDomain,
    ResultProductDomain,
)
from shopping_bot.core.domains.request_domain import (
    InputRequestDomain,
    ResponseRequestDomain,
)
from shopping_bot.core.domains.user_domain import InputUserDomain, ResultUserDomain
from shopping_bot.core.records.product_records import ResponseProductRecord
from shopping_bot.core.records.request_records import ResponseRequestRecord
from shopping_bot.core.records.user_records import ResponseUserRecord


class UserControllerInterface(Protocol):
    async def start_cmd(self, user: InputUserDomain) -> ResultUserDomain: ...
    async def get_user_id_by_telegram_id(self, user_telegram_id: int) -> int | None: ...


class ProductControllerInterface(Protocol):
    async def process_product(self, naem: str) -> ResultProductDomain: ...
    async def process_confirmation(
        self, confirmed: bool, product_id: int | None, product_name: str | None
    ) -> ResultProductDomain: ...
    async def process_unit(self, unit_str: str, name: str) -> ResultProductDomain: ...


class RequestControllerInterface(Protocol):
    async def process_quantity(
        self, product_id: int, quantity: str, user_id: int
    ) -> ResponseRequestDomain: ...


class UserRepositoryInterface(Protocol):
    async def get_user_by_telegram_id(
        self, user_telegram_id: int
    ) -> ResponseUserRecord | None: ...

    async def save_user(self, user: InputUserDomain) -> ResponseUserRecord: ...


class ProductRepositoryInterface(Protocol):
    async def get_products(self) -> list[ResponseProductRecord]: ...
    async def get_product(self, id: int) -> ResponseProductRecord: ...
    async def create_product(
        self, product: InputProductDomain
    ) -> ResponseProductRecord: ...


class RequestRepositoryInterface(Protocol):
    async def create_request(
        self, request: InputRequestDomain
    ) -> ResponseRequestRecord: ...
