from unittest.mock import AsyncMock, MagicMock

import pytest

from shopping_bot.core.records.user_records import ResponseUserRecord


@pytest.fixture
def mock_message_factory():
    def _make(from_user=None, text=None):
        message = MagicMock()
        message.from_user = from_user
        message.answer = AsyncMock()
        message.text = text

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
def mock_user_controller():
    user_controller = MagicMock()
    user_controller.start_cmd = AsyncMock()

    return user_controller


@pytest.fixture
def mock_repository_factory():
    def _make(
        save_user_response: ResponseUserRecord,
        user_record: ResponseUserRecord | None = None,
    ):
        repository = MagicMock()
        repository.get_user_by_telegram_id = AsyncMock()
        repository.get_user_by_telegram_id.return_value = user_record
        repository.save_user = AsyncMock()
        repository.save_user.return_value = save_user_response
        return repository

    return _make


@pytest.fixture
def mock_async_session_factory():
    session = AsyncMock()
    factory = MagicMock(return_value=session)
    session.__aenter__.return_value = session
    session.__aexit__.return_value = None
    return factory, session


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
def mock_response():
    response = AsyncMock()
    response.product_id = 1
    response.product_name = "milk"
    response.quantity = 10
    response.units = "kilo"
    return response
