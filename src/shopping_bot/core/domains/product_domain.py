from dataclasses import dataclass
from decimal import Decimal
from enum import Enum, auto


class ProductInputResult(Enum):
    PRODUCT_FOUND = auto()
    PRODUCT_NOT_FOUND_NEEDS_CONFIRMATION = auto()
    PRODUCT_CREATED = auto()
    UNIT_ACCEPTED = auto()
    INVALID_UNIT = auto()


@dataclass
class ResultProductDomain:
    result: ProductInputResult
    product_id: int | None = None
    product_name: str | None = None
    quantity: Decimal | None = None
    unit: str | None = None


@dataclass
class ResponseProductDomain:
    id: int
    name: str
    unit: str
    description: str | None = None


@dataclass
class InputProductDomain:
    name: str
    unit: str | None = None
    description: str | None = None
