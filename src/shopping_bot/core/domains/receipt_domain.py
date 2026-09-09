from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

from shopping_bot.core.records.utils import RequestStatus


@dataclass
class InputStoreDomain:
    name: str
    address: str


@dataclass
class InputReceiptDomain:
    store_id: int | None
    uploaded_by_user_id: int | None
    receipt_date: datetime
    image_url: str | None
    raw_model_response: str | None
    created_at: datetime


@dataclass
class ResponseReceiptDomain:
    id: int
    store_id: int | None
    uploaded_by_user_id: int
    receipt_date: datetime
    image_url: str | None
    raw_model_response: str | None
    created_at: datetime


@dataclass
class Try_Input_Receipt_Domain:
    id: int
    receipt_id: int
    price: Decimal
    quantity: Decimal
    match_confidence: int
    status: RequestStatus
    store_id: int
    uploaded_by_user_id: int
    raw_model_response: str | None
