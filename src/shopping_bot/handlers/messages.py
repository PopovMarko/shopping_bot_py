from enum import Enum

from shopping_bot.core.domains.history_domain import (
    LastShoppingDomain,
    StatisticsRequest,
    StatisticsShoppingDomain,
)
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


def last_shopping_domain_to_string(last_shopping: LastShoppingDomain) -> str:
    list_product_strings: list[str] = []
    for p in last_shopping.products:
        list_product_strings.append(
            f"{p.name} {p.quantity} {p.price} {p.quantity * p.price}"
        )
    return f"{last_shopping.last_shopping_date}\n\
            Пользователь {last_shopping.user_name}\n\
            в магазине {last_shopping.store_name} \
            купил:\n\
            {'\n'.join(list_product_strings)}"


def statistics_shopping_to_string(
    stat_shopping: StatisticsShoppingDomain,
) -> str:
    list_product_group: list[str] = []
    for g in stat_shopping.product_groups:
        list_product_group.append(
            f"{g.product_name}      {g.product_quantity} {g.product_cost}"
        )
    return f"За крайние 30 дней было совершено {stat_shopping.shoppings_ammount}\n\
                покупок на сумму {stat_shopping.expences_ammount} :\n\
            {'\n'.join(list_product_group)}"
