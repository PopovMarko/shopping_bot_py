from unittest.mock import AsyncMock, MagicMock

import pytest
from aiogram.types import Message


@pytest.fixture
def mock_bot_info():
    bot_info = MagicMock()
    bot_info.username = AsyncMock()
    bot_info.username.return_value = "shopping_bot"
    return bot_info


@pytest.fixture
def mock_bot():
    bot = MagicMock()
    bot.get_me = AsyncMock()
    return bot


@pytest.fixture
def mock_product_controller():
    product_controller = MagicMock()
    product_controller.process_quantity = AsyncMock()
    product_controller.process_product = AsyncMock()
    product_controller.process_confirmation = AsyncMock()
    return product_controller


@pytest.fixture
def mock_state():
    state = AsyncMock()
    state.set_state = AsyncMock()
    state.update_data = AsyncMock()
    state.get_vale = AsyncMock()
    return state


@pytest.fixture
def mock_request_controller():
    controller = AsyncMock()
    controller.process_quantity = AsyncMock()
    controller.process_request_list = AsyncMock()

    return controller


@pytest.fixture
def mock_callback_query():
    query = MagicMock()
    query.data = MagicMock()
    query.data.return_value = "cart_1"
    query.answer = AsyncMock()
    query.message = MagicMock(spec=Message)
    query.message.edit_reply_markup = AsyncMock()

    return query
