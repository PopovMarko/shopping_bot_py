from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from enum import Enum, auto

from shopping_bot.core.domains.product_domain import ResponseProductDomain
from shopping_bot.core.domains.user_domain import ResponseUserDomain
from shopping_bot.core.records.utils import RequestStatus


class RequestInputResult(Enum):
    QUANTITY_ACCEPTED = auto()
    INVALID_QUANTITY = auto()


@dataclass
class ResultRequestDomain:
    result: RequestInputResult
    request_domain: ResponseRequestDomain | None


@dataclass
class InputRequestDomain:
    product_id: int
    requested_by_user_id: int
    requested_quantity: int
    requested_at: datetime
    quantity: Decimal | None
    status: RequestStatus | None = None


@dataclass
class ResponseRequestDomain:
    id: int
    product_id: int
    requested_by_user_id: int
    requested_quantity: Decimal
    requested_at: datetime
    product: ResponseProductDomain
    requested_by_user: ResponseUserDomain
    status: RequestStatus | None = None


@dataclass
class ResponseStoreDomain:
    id: int | None
    name: str
    address: str | None
