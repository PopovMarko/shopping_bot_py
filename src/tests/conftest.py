from unittest.mock import AsyncMock, MagicMock

import pytest

from shopping_bot.core.repository_dto import UserRecord


@pytest.fixture
def mock_message_factory():
    def _make(from_user=None):
        message = MagicMock()
        message.from_user = from_user
        message.answer = AsyncMock()

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
    def _make(save_user_response: UserRecord, user_record: UserRecord | None = None):
        repository = MagicMock()
        repository.get_user_by_telegram_id = AsyncMock()
        repository.get_user_by_telegram_id.return_value = user_record
        repository.save_user = AsyncMock()
        repository.save_user.return_value = save_user_response
        return repository

    return _make
