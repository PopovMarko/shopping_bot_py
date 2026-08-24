from dataclasses import dataclass
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
