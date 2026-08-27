from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from enum import Enum, auto

from shopping_bot.db.models import RequestStatus


class UserRegistrationResult(Enum):
    REGISTERED_USER = auto()
    REGISTER_USER_SUCCESS = auto()


@dataclass
class RequestUserDomain:
    telegram_id: int
    name: str
    is_admin: bool = False


@dataclass
class UserDomain:
    msg: UserRegistrationResult
    id: int
    telegram_id: int
    name: str


class ProductInputResult(Enum):
    PRODUCT_FOUND = auto()
    PRODUCT_NOT_FOUND_NEEDS_CONFIRMATION = auto()
    PRODUCT_CREATED = auto()


class RequestInputResult(Enum):
    QUANTITY_ACCEPTED = auto()
    INVALID_QUANTITY = auto()


@dataclass
class ProductDomain:
    result: ProductInputResult
    product_id: int | None = None
    product_name: str | None = None
    quantity: Decimal | None = None
    unit: str | None = None


@dataclass
class RequestDomain:
    result: RequestInputResult
    product: ProductDomain
    user: UserDomain
    quantity: Decimal
    registered_at: datetime
    status: RequestStatus
