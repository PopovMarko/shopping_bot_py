from unittest.mock import MagicMock, patch

import pytest

from shopping_bot.core.domains.user_domain import InputUserDomain
from shopping_bot.core.records.user_records import ResponseUserRecord
from shopping_bot.db.repository.user_repository import UserRepository


@pytest.mark.asyncio
async def test_get_user_by_telegram_id_found(mock_async_session_factory):
    factory, session = mock_async_session_factory

    mock_user_model = MagicMock(
        id=1,
        telegram_id=123,
        is_admin=False,
        shopping_status=False,
        active_message_id=None,
        shopping_started_at=None,
    )

    mock_user_model.name = "Marko"

    result = MagicMock()
    result.scalar_one_or_none.return_value = mock_user_model

    session.execute.return_value = result

    with patch(
        "shopping_bot.db.repository.user_repository.async_session_factory", factory
    ):
        repository = UserRepository()
        res = await repository.get_user_by_telegram_id(123)

    assert res == ResponseUserRecord(
        id=1,
        telegram_id=123,
        name="Marko",
        is_admin=False,
        shopping_status=False,
        active_message_id=None,
        shopping_started_at=None,
    )

    session.execute.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_user_by_telegram_id_not_found(mock_async_session_factory):
    factory, session = mock_async_session_factory

    result = MagicMock()
    result.scalar_one_or_none.return_value = None
    session.execute.return_value = result

    with patch(
        "shopping_bot.db.repository.user_repository.async_session_factory", factory
    ):
        repository = UserRepository()
        res = await repository.get_user_by_telegram_id(123)

    assert res is None
    session.execute.assert_awaited_once()


@pytest.mark.asyncio
async def test_save_user(mock_async_session_factory):
    factory, session = mock_async_session_factory

    mock_user_model = MagicMock(
        id=1,
        telegram_id=123,
        is_admin=False,
        shopping_status=False,
        active_message_id=None,
        shopping_started_at=None,
    )

    mock_user_model.name = "Marko"

    result = MagicMock()
    result.scalar_one.return_value = mock_user_model

    session.execute.return_value = result

    with patch(
        "shopping_bot.db.repository.user_repository.async_session_factory", factory
    ):
        user_domain = InputUserDomain(
            telegram_id=123,
            name="Marko",
            is_admin=False,
        )

        repository = UserRepository()
        res = await repository.save_user(user_domain)

    assert res == ResponseUserRecord(
        id=1,
        telegram_id=123,
        name="Marko",
        is_admin=False,
        shopping_status=False,
        active_message_id=None,
        shopping_started_at=None,
    )
    session.execute.assert_awaited_once()
