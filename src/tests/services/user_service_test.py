import pytest

from shopping_bot.core.domains.user_domain import (
    InputUserDomain,
    ResultUserDomain,
    UserRegistrationResult,
)
from shopping_bot.core.records.user_records import ResponseUserRecord
from shopping_bot.services.user_service import UserService

user = ResponseUserRecord(
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
            ResultUserDomain(
                msg=UserRegistrationResult.REGISTER_USER_SUCCESS,
                id=1,
                telegram_id=123,
                name="Marko",
            ),
        ),
        (
            user,
            ResultUserDomain(
                msg=UserRegistrationResult.REGISTERED_USER,
                id=1,
                telegram_id=123,
                name="Marko",
            ),
        ),
    ],
)
async def test_start_cmd_user_exists_and_not_exists(
    mock_user_repository_factory, user_record, expected
):
    user1 = InputUserDomain(telegram_id=123, name="Marko")
    mock_repository = mock_user_repository_factory(user, user_record)

    service = UserService(mock_repository)
    res = await service.start_cmd(user1)

    mock_repository.get_user_by_telegram_id.assert_awaited_once_with(123)
    if user_record is None:
        mock_repository.save_user.assert_awaited_once_with(user1)
    else:
        mock_repository.save_user.assert_not_awaited()

    assert res == expected
