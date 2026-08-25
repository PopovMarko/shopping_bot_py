from dataclasses import dataclass
from datetime import datetime


@dataclass
class UserRecord:
    id: int
    telegram_id: int
    name: str
    is_admin: bool
    shopping_status: bool
    active_message_id: int | None
    shopping_started_at: datetime | None
