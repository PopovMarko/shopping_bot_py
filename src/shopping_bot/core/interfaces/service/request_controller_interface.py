from decimal import Decimal
from typing import Protocol

from shopping_bot.core.domains.product_domain import ResponseProductDomain
from shopping_bot.core.domains.request_domain import (
    ResponseRequestDomain,
    ResultRequestDomain,
)
from shopping_bot.core.records.utils import RequestStatus


class RequestControllerInterface(Protocol):
    async def process_quantity(
        self, product_id: int, quantity_str: str, telegram_user_id: int
    ) -> ResultRequestDomain: ...

    async def process_request_list(
        self, *args: RequestStatus
    ) -> list[ResponseRequestDomain]: ...

    async def process_request_in_cart_and_back(
        self, request_id: int
    ) -> list[ResponseRequestDomain]: ...

    async def process_request_from_receipt(
        self,
        product: ResponseProductDomain,
        requested_by_user_id: int,
        quantity: Decimal | None,
    ) -> ResponseRequestDomain: ...


class ReceiptControllerInterface(Protocol):
    async def process_receipt(
        self,
        img_bytes_64: str,
        user_telegram_id: int,
        request_domain_list: list[ResponseRequestDomain],
    ) -> None: ...

    async def process_empty_receipt(
        self, user_telegram_id: int, request_domain_list: list[ResponseRequestDomain]
    ) -> None: ...
