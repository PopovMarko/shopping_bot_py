from typing import Iterable, Protocol

from shopping_bot.core.domains.product_domain import (
    InputProductDomain,
    ResultProductDomain,
)
from shopping_bot.core.domains.request_domain import (
    InputRequestDomain,
    ResponseRequestDomain,
    ResultRequestDomain,
)
from shopping_bot.core.domains.user_domain import InputUserDomain, ResultUserDomain
from shopping_bot.core.records.product_records import ResponseProductRecord
from shopping_bot.core.records.request_records import ResponseRequestRecord
from shopping_bot.core.records.user_records import ResponseUserRecord
from shopping_bot.core.records.utils import RequestStatus


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
    ) -> ResultRequestDomain: ...
    async def process_request_list(
        self, *args: RequestStatus
    ) -> list[ResponseRequestDomain]: ...
    async def process_request_by_id(self, request_id: int) -> ResponseRequestDomain: ...
    async def process_request_in_cart_and_back(
        self, request_id: int
    ) -> list[ResponseRequestDomain]: ...


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
    async def get_request_list(
        self, *args: RequestStatus
    ) -> list[ResponseRequestRecord]: ...
    async def get_request_by_id(self, request_id: int) -> ResponseRequestRecord: ...
    async def update_request_status(
        self, request_id: int, statuse: RequestStatus
    ) -> None: ...


class InStoreControllerInterface(Protocol):
    async def process_in_store(self) -> None: ...
