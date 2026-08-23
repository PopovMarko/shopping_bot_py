from enum import Enum

from shopping_bot.core.domain import ResponseUserDomain, UserRegistrationResult

HELP_MESSAGE = """
/start - user User registration
/help - this message
"""


class ErrorMessage(Enum):
    INVALID_USER = "Invalid user ID or user name"


def user_domain_to_string(response: ResponseUserDomain) -> str:
    match response.msg:
        case UserRegistrationResult.REGISTERED_USER:
            return f"Welcome back {response.name}"
        case UserRegistrationResult.REGISTER_USER_SUCCESS:
            return f"Welcome {response.name}, \nnow you are registered user"
        case _:
            raise ValueError
