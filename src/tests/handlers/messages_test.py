from datetime import datetime
from decimal import Decimal

import pytest

from shopping_bot.core.domains.history_domain import (
    LastShoppingDomain,
    LastShoppingRequestDomain,
    StatisticsRequest,
)
from shopping_bot.core.domains.user_domain import (
    ResultUserDomain,
    UserRegistrationResult,
)
from shopping_bot.handlers.messages import (
    last_shopping_domain_to_string,
    statistics_shopping_to_string,
    user_domain_to_string,
)


@pytest.mark.parametrize(
    "status, response_string",
    [
        (
            UserRegistrationResult.REGISTER_USER_SUCCESS,
            "Welcome Marko, \nnow you are registered user",
        ),
        (UserRegistrationResult.REGISTERED_USER, "Welcome back Marko"),
    ],
)
def test_user_domain_to_string(status, response_string):
    user_domain = ResultUserDomain(status, 1, 123, "Marko")
    res = user_domain_to_string(user_domain)
    assert res == response_string


def test_last_shopping_domain_to_string():
    last_shopping = LastShoppingDomain(
        user_name="Marko",
        last_shopping_date=datetime(2026, 9, 28, 14, 35),
        store_name="Lidl",
        products=[
            LastShoppingRequestDomain("milk", "l", Decimal("2.000"), Decimal("1.50")),
            LastShoppingRequestDomain("bread", "шт", None, None),
        ],
    )

    assert last_shopping_domain_to_string(last_shopping) == (
        "28.09.2026 14:35\n"
        "Пользователь Marko\n"
        "в магазине Lidl купил:\n"
        "milk 2 l x 1.50 = 3.00\n"
        "bread\n"
        "Итого: 3.00"
    )


def test_last_shopping_domain_to_string_without_date():
    last_shopping = LastShoppingDomain(
        user_name="Marko", last_shopping_date=None, store_name="", products=[]
    )

    assert last_shopping_domain_to_string(last_shopping).startswith("Дата неизвестна")


def test_statistics_shopping_to_string():
    stat_shopping = [
        StatisticsRequest("milk", Decimal("2.500"), Decimal("7.50")),
        StatisticsRequest("bread", Decimal(0), Decimal(0)),
    ]

    assert statistics_shopping_to_string(stat_shopping) == (
        "За последние 30 дней куплено товаров: 2\n"
        "на сумму 7.50:\n"
        "milk: 7.50 (2.5)\n"
        "bread: 0.00 (0)"
    )


def test_statistics_shopping_to_string_empty():
    assert statistics_shopping_to_string([]) == "За последние 30 дней покупок нет"
