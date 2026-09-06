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
    user: ResponseUserRecord
    product: ResponseProductRecord
    purchased_by_user: ResponseUserRecord | None
    receipt: ResponseReceiptRecord | None
    price: Decimal | None
    quantity: Decimal | None
    match_confidence: int | None


@dataclass
class ResponseStoreRecord:
    id: int
    name: str
    address: str


@dataclass
class ResponseReceiptRecord:
    id: int
    store: ResponseStoreRecord
    uploaded_by_user: ResponseUserRecord
    receipt_date: datetime
    image_url: str | None
    raw_model_response: str | None
    created_at: datetime
