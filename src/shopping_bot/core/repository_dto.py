from dataclasses import dataclass
from datetime import datetime

from shopping_bot.db.models import RequestStatus


@dataclass
class UserRecord:
    id: int
    telegram_id: int
    name: str
    is_admin: bool
    shopping_status: bool
    active_message_id: int | None
    shopping_started_at: datetime | None


@dataclass
class ProductRecord:
    id: int
    name: str
    description: str | None
    unit: str


@dataclass
class RequestRecord:
    id: int
    product: ProductRecord
    user: UserRecord
    requested_quantity: int
    requested_at: datetime
    status: RequestStatus
