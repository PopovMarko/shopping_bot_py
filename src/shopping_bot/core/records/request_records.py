from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

from shopping_bot.core.records.product_records import ResponseProductRecord
from shopping_bot.core.records.user_records import ResponseUserRecord
from shopping_bot.core.records.utils import RequestStatus


@dataclass
class ResponseRequestRecord:
    id: int
    requested_quantity: Decimal
    requested_at: datetime
    status: RequestStatus
    requested_by_user_id: int
    product_id: int
    receipt_id: int | None
    price: Decimal | None
    quantity: Decimal | None
    match_confidence: int | None
    product: ResponseProductRecord
    requested_by_user: ResponseUserRecord


@dataclass
class ResponseStoreRecord:
    id: int
    name: str
    address: str


@dataclass
class ResponseReceiptRecord:
    id: int
    store_id: int | None
    uploaded_by_user_id: int
    receipt_date: datetime
    image_url: str | None
    raw_model_response: str | None
    created_at: datetime
