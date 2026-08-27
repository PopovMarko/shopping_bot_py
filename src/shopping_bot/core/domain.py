from dataclasses import dataclass
from decimal import Decimal
from enum import Enum, auto


class UserRegistrationResult(Enum):
    REGISTERED_USER = auto()
    REGISTER_USER_SUCCESS = auto()


@dataclass
class RequestUserDomain:
    telegram_id: int
    name: str
    is_admin: bool = False


@dataclass
class ResponseUserDomain:
    msg: UserRegistrationResult
    id: int
    telegram_id: int
    name: str


class ProductInputResult(Enum):
    PRODUCT_FOUND = auto()
    PRODUCT_NOT_FOUND_NEEDS_CONFIRMATION = auto()
    PRODUCT_CREATED = auto()
    QUANTITY_ACCEPTED = auto()
    INVALID_QUANTITY = auto()


@dataclass
class ResponseProductDomain:
    result: ProductInputResult
    product_id: int | None = None
    product_name: str | None = None
    suggested_product_id: int | None = None
    suggested_name: str | None = None
    quantity: Decimal | None = None
    units: str | None = None
