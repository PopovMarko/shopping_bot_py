from datetime import datetime
from decimal import Decimal

import pytest

from shopping_bot.core.domains.product_domain import ResponseProductDomain
from shopping_bot.core.domains.request_domain import ResponseRequestDomain
from shopping_bot.core.domains.user_domain import ResponseUserDomain
from shopping_bot.core.records.utils import RequestStatus
from shopping_bot.keyboards.in_store_kbd import get_inline_product_list_keyboard
from shopping_bot.keyboards.main_kbd import (
    get_cancel_inline_keyboard,
    get_go_to_privat_inline_keyboard,
    get_go_to_privat_keyboard,
)


def _request(status):
    return ResponseRequestDomain(
        id=5,
        product_id=1,
        requested_by_user_id=1,
        requested_quantity=Decimal(2),
        requested_at=datetime(2026, 9, 28),
        quantity=None,
        price=None,
        product=ResponseProductDomain(id=1, name="milk", unit="l"),
        requested_by_user=ResponseUserDomain(
            id=1,
            telegram_id=123,
            name="Marko",
            is_admin=False,
            shopping_status=False,
            active_message_id=None,
            shopping_started_at=None,
        ),
        status=status,
    )


@pytest.mark.parametrize(
    "status, checkbox",
    [
        (RequestStatus.pending, "⬜"),
        (RequestStatus.in_cart, "✅"),
        (RequestStatus.fulfilled, "✅"),
        (RequestStatus.cancelled, "❌"),
        (None, "E"),
    ],
)
def test_inline_product_list_keyboard(status, checkbox):
    keyboard = get_inline_product_list_keyboard([_request(status)])

    product_button, stop_button = [row[0] for row in keyboard.inline_keyboard]
    assert product_button.text == f"{checkbox} milk 2 l"
    assert product_button.callback_data == "cart_5"
    assert stop_button.callback_data == "stop"


def test_cancel_inline_keyboard():
    keyboard = get_cancel_inline_keyboard()
    assert keyboard.inline_keyboard[0][0].callback_data == "cancel"


def test_go_to_privat_keyboard():
    keyboard = get_go_to_privat_keyboard("https://t.me/bot")
    assert [row[0].text for row in keyboard.keyboard] == ["Перейти в личку", "Отмена"]


def test_go_to_privat_inline_keyboard():
    keyboard = get_go_to_privat_inline_keyboard("https://t.me/bot")
    buttons = keyboard.inline_keyboard[0]
    assert buttons[0].url == "https://t.me/bot"
    assert buttons[1].callback_data == "cancel"
