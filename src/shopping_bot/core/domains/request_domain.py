from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from enum import Enum, auto

from shopping_bot.core.domains.product_domain import (
    ResponseProductDomain,
)
from shopping_bot.core.domains.user_domain import ResponseUserDomain
from shopping_bot.core.records.utils import RequestStatus


class RequestInputResult(Enum):
    QUANTITY_ACCEPTED = auto()
    INVALID_QUANTITY = auto()


@dataclass
class ResultRequestDomain:
    result: RequestInputResult
    product: ResponseProductDomain | None = None
    user: ResponseUserDomain | None = None
    user_id: int | None = None
    quantity: Decimal | None = None
    requested_at: datetime | None = None
    status: RequestStatus | None = None


@dataclass
class InputRequestDomain:
    product_id: int
    requested_by_user_id: int
    requested_quantity: int
    requested_at: datetime
    status: RequestStatus | None = None


@dataclass
class ResponseRequestDomain:
    id: int
    product: ResponseProductDomain
    requested_by_user: ResponseUserDomain
    requested_quantity: Decimal
    requested_at: datetime
    status: RequestStatus | None = None
