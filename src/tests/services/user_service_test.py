from unittest.mock import AsyncMock, MagicMock

import pytest

from shopping_bot.core.domain import (
    RequestUserDomain,
    ResponseUserDomain,
    UserRegistrationResult,
)
from shopping_bot.core.repository_dto import UserRecord
from shopping_bot.services.user_service import UserService

user = UserRecord(
    id=1,
    telegram_id=123,
    name="Marko",
    is_admin=False,
    shopping_status=False,
    active_message_id=2,
    shopping_started_at=None,
)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "user_record, expected",
    [
        (
            None,
            ResponseUserDomain(
                msg=UserRegistrationResult.REGISTER_USER_SUCCESS,
                id=1,
                telegram_id=123,
                name="Marko",
            ),
        ),
        (
            user,
            ResponseUserDomain(
                msg=UserRegistrationResult.REGISTERED_USER,
                id=1,
                telegram_id=123,
                name="Marko",
            ),
        ),
    ],
)
async def test_start_cmd_user_exists_and_not_exists(
    mock_repository_factory, user_record, expected
):
    user1 = RequestUserDomain(telegram_id=123, user_name="Marko")
    mock_repository = mock_repository_factory(user, user_record)

    service = UserService(mock_repository)
    res = await service.start_cmd(user1)

    mock_repository.get_user_by_telegram_id.assert_awaited_once_with(123)
    if user_record is None:
        mock_repository.save_user.assert_awaited_once_with(user1)
    else:
        mock_repository.save_user.assert_not_awaited()

    assert res == expected
