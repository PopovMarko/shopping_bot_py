from typing import Protocol

from shopping_bot.core.domains.request_domain import (
    ResponseRequestDomain,
    ResultRequestDomain,
)
from shopping_bot.core.records.utils import RequestStatus


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
