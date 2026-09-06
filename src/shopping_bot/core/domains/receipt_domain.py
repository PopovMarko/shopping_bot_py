from dataclasses import dataclass
from datetime import datetime

from shopping_bot.core.domains.request_domain import ResponseStoreDomain
from shopping_bot.core.domains.user_domain import ResponseUserDomain


@dataclass
class InputStoreDomain:
    name: str
    address: str


@dataclass
class InputReceiptDomain:
    store: ResponseStoreDomain
    uploaded_by_user: ResponseUserDomain
    receipt_date: datetime
    image_url: str | None
    raw_model_response: str | None
    created_at: datetime


@dataclass
class ResponseReceiptDomain:
    id: int
    store_id: int
    uploaded_by_user_id: int
    receipt_date: datetime
    image_url: str | None
    raw_model_response: str | None


@dataclass
class InputReceiptDbDomain:
    store_id: int
    uploaded_by_user_id: int
    receipt_date: datetime
    image_url: str | None
    raw_model_response: str | None
    created_at: datetime
