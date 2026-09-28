from datetime import datetime
from decimal import Decimal
from unittest.mock import AsyncMock, MagicMock

import pytest

from shopping_bot.core.domains.history_domain import (
    LastShoppingDomain,
    LastShoppingRequestDomain,
    StatisticsRequest,
)
from shopping_bot.handlers.history import (
    history,
    last_shopping,
    return_to_main_menu,
    statistics_shopping,
)
from shopping_bot.keyboards.history_kbd import get_history_keyboard
from shopping_bot.keyboards.main_kbd import get_main_keyboard
from shopping_bot.states.user_states import WaitFor


@pytest.fixture
def mock_history_controller():
    controller = MagicMock()
    controller.process_last_shopping = AsyncMock(
        return_value=LastShoppingDomain(
            user_name="Marko",
            last_shopping_date=datetime(2026, 9, 28, 14, 35),
            store_name="Lidl",
            products=[
                LastShoppingRequestDomain("milk", "l", Decimal(2), Decimal("1.50"))
            ],
        )
    )
    controller.process_statistics_shopping = AsyncMock(
        return_value=[StatisticsRequest("milk", Decimal(2), Decimal("3.00"))]
    )
    return controller


@pytest.mark.asyncio
async def test_history(mock_message_factory, mock_state):
    message = mock_message_factory()

    await history(message, mock_state)

    mock_state.set_state.assert_awaited_once_with(WaitFor.history_type)
    message.answer.assert_awaited_once_with(
        "Нажмите кнопку", reply_markup=get_history_keyboard()
    )


@pytest.mark.asyncio
async def test_return_to_main_menu(mock_message_factory, mock_state):
    message = mock_message_factory()

    await return_to_main_menu(message, mock_state)

    mock_state.clear.assert_awaited_once()
    message.answer.assert_awaited_once_with(
        "Главное меню", reply_markup=get_main_keyboard()
    )


@pytest.mark.asyncio
async def test_last_shopping(
    mock_message_factory, mock_state, mock_user, mock_history_controller
):
    message = mock_message_factory(from_user=mock_user)

    await last_shopping(message, mock_state, mock_history_controller)

    mock_history_controller.process_last_shopping.assert_awaited_once_with(
        user_telegram_id=mock_user.id
    )
    text = message.answer.await_args.args[0]
    assert "28.09.2026 14:35" in text
    assert "Marko" in text
    assert "Lidl" in text
    assert "milk 2 l x 1.50 = 3.00" in text


@pytest.mark.asyncio
async def test_last_shopping_without_user(
    mock_message_factory, mock_state, mock_history_controller
):
    message = mock_message_factory(from_user=None)

    with pytest.raises(ValueError):
        await last_shopping(message, mock_state, mock_history_controller)


@pytest.mark.asyncio
async def test_statistics_shopping(
    mock_message_factory, mock_state, mock_history_controller
):
    message = mock_message_factory()

    await statistics_shopping(message, mock_state, mock_history_controller)

    mock_history_controller.process_statistics_shopping.assert_awaited_once()
    text = message.answer.await_args.args[0]
    assert "milk" in text
