from enum import Enum

from shopping_bot.core.domains.request_domain import ResponseRequestDomain
from shopping_bot.core.domains.user_domain import (
    ResultUserDomain,
    UserRegistrationResult,
)

HELP_MESSAGE = "/start - user User registration\n/help - this message"


class ErrorMessage(Enum):
    INVALID_USER = "Invalid user ID or user name"


def user_domain_to_string(response: ResultUserDomain) -> str:
    match response.msg:
        case UserRegistrationResult.REGISTERED_USER:
            return f"Welcome back {response.name}"
        case UserRegistrationResult.REGISTER_USER_SUCCESS:
            return f"Welcome {response.name}, \nnow you are registered user"
        case _:
            raise ValueError


def list_response_request_domain_to_string(
    product_list: list[ResponseRequestDomain],
) -> str:
    res_list = []
    for p in product_list:
        res_list.append(
            f"{p.requested_by_user.name} {p.product.name} {p.requested_quantity} {p.product.unit}"
        )
    return "\n".join(res_list)
