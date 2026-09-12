from unittest.mock import AsyncMock, MagicMock

import pytest


@pytest.fixture
def mock_message_factory():
    def _make(from_user=None, text=None, chat_type="privat"):
        message = MagicMock()
        message.from_user = from_user
        message.answer = AsyncMock()
        message.text = text
        message.chat.type = chat_type

        return message

    return _make


@pytest.fixture
def mock_user():
    user = MagicMock()
    user.id = 1
    user.telegram_id = 123
    user.first_name = "Marko"

    return user


@pytest.fixture
def mock_async_session_factory():
    session = AsyncMock()
    factory = MagicMock(return_value=session)
    session.__aenter__.return_value = session
    session.__aexit__.return_value = None
    return factory, session


@pytest.fixture
def mock_response():
    response = AsyncMock()
    response.product_id = 1
    response.product_name = "milk"
    response.quantity = 10
    response.units = "kilo"
    return response


@pytest.fixture
def mock_user_controller():
    user_controller = MagicMock()
    user_controller.start_cmd = AsyncMock()
    user_controller.get_user_id_by_telegram_id = AsyncMock()
    return user_controller
