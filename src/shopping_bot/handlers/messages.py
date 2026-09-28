from decimal import Decimal
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


def _format_quantity(quantity: Decimal) -> str:
    return f"{quantity:.3f}".rstrip("0").rstrip(".")


def last_shopping_domain_to_string(last_shopping: LastShoppingDomain) -> str:
    list_product_strings: list[str] = []
    total_cost = Decimal(0)
    for p in last_shopping.products:
        # products closed without receipt have no price and quantity
        if p.quantity is None or p.price is None:
            list_product_strings.append(p.name)
            continue
        cost = p.quantity * p.price
        total_cost += cost
        list_product_strings.append(
            f"{p.name} {_format_quantity(p.quantity)} {p.unit} x {p.price} = {cost:.2f}"
        )
    shopping_date = last_shopping.last_shopping_date
    header = [
        f"{shopping_date:%d.%m.%Y %H:%M}" if shopping_date else "Дата неизвестна",
        f"Пользователь {last_shopping.user_name}",
        f"в магазине {last_shopping.store_name} купил:",
    ]
    return "\n".join([*header, *list_product_strings, f"Итого: {total_cost:.2f}"])


def statistics_shopping_to_string(
    stat_shopping: list[StatisticsRequest],
) -> str:
    if not stat_shopping:
        return "За последние 30 дней покупок нет"
    list_product_group: list[str] = []
    total_cost = Decimal(0)
    for g in stat_shopping:
        quantity = _format_quantity(g.product_quantity)
        list_product_group.append(
            f"{g.product_name}: {g.product_cost:.2f} ({quantity})"
        )
        total_cost += g.product_cost
    header = (
        f"За последние 30 дней куплено товаров: {len(stat_shopping)}\n"
        f"на сумму {total_cost:.2f}:\n"
    )
    return header + "\n".join(list_product_group)
