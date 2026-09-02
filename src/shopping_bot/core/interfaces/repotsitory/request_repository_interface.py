from typing import Protocol

from shopping_bot.core.domains.request_domain import (
    InputRequestDomain,
)
from shopping_bot.core.records.request_records import ResponseRequestRecord
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
