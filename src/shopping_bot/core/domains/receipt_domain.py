from dataclasses import dataclass
from datetime import datetime


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
