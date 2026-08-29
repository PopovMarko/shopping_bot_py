from dataclasses import dataclass
from datetime import datetime
from enum import Enum, auto


class UserRegistrationResult(Enum):
    REGISTERED_USER = auto()
    REGISTER_USER_SUCCESS = auto()


@dataclass
class InputUserDomain:
    telegram_id: int
    name: str
    is_admin: bool = False


@dataclass
class ResultUserDomain:
    msg: UserRegistrationResult
    id: int
    telegram_id: int
    name: str


# TODO fields purchases and requests
@dataclass
class ResponseUserDomain:
    id: int
    telegram_id: int
    name: str
    is_admin: bool
    shopping_status: bool
    active_message_id: int | None
    shopping_started_at: datetime | None
