from typing import Protocol

from shopping_bot.core.domains.receipt_domain import (
    InputReceiptDomain,
)
from shopping_bot.core.domains.request_domain import (
    InputRequestDomain,
)
from shopping_bot.core.records.request_records import (
    ResponseReceiptRecord,
    ResponseRequestRecord,
    ResponseStoreRecord,
)
from shopping_bot.core.records.utils import RequestStatus


class RequestRepositoryInterface(Protocol):
    async def create_request(
        self, request: InputRequestDomain
    ) -> ResponseRequestRecord: ...

    async def get_request_list(
        self, *args: RequestStatus
    ) -> list[ResponseRequestRecord]: ...

    async def get_request_by_id(self, request_id: int) -> ResponseRequestRecord: ...

    async def update_request_status(
        self, request_id: int, status: RequestStatus
    ) -> None: ...


class ReceiptRepositoryInterface(Protocol):
    async def create_receipt(
        self, receipt: InputReceiptDomain
    ) -> ResponseReceiptRecord: ...

    async def get_product_name_list(self, request_id_list: list[int]) -> list[str]: ...

    async def get_store_by_name_and_address(
        self,
        name: str,
        address: str,
    ) -> ResponseStoreRecord | None: ...

    async def create_store(self, name: str, address: str) -> ResponseStoreRecord: ...
    async def update_receipt(self) -> None: ...
