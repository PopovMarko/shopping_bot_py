from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from enum import Enum, auto

from shopping_bot.core.domains.product_domain import ResultProductDomain
from shopping_bot.core.domains.user_domain import ResponseUserDomain
from shopping_bot.db.models import RequestStatus


class RequestInputResult(Enum):
    QUANTITY_ACCEPTED = auto()
    INVALID_QUANTITY = auto()


@dataclass
class ResultRequestDomain:
    result: RequestInputResult
    product: ResultProductDomain | None = None
    user_id: int | None = None
    quantity: Decimal | None = None
    registered_at: datetime | None = None
    status: RequestStatus | None = None


@dataclass
class InputRequestDomain:
    product_id: int
    requested_by_user_id: int
    requested_quantity: int
    registered_at: datetime
    status: RequestStatus | None = None


@dataclass
class ResponseRequestDomain:
    id: int
    product_id: int
    requested_by_user: ResponseUserDomain
    requested_quantity: Decimal
    registered_at: datetime
    status: RequestStatus | None = None
