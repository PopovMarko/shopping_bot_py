import pytest

from shopping_bot.core.domain import (
    RequestUserDomain,
    UserDomain,
    UserRegistrationResult,
)
from shopping_bot.handlers.base import start
from shopping_bot.handlers.messages import ErrorMessage


@pytest.mark.asyncio
async def test_start_when_from_user_is_none(mock_message_factory, mock_user_controller):
    mock_message = mock_message_factory(from_user=None)

    await start(mock_message, mock_user_controller)

    mock_message.answer.assert_awaited_once_with(ErrorMessage.INVALID_USER.value)
    mock_user_controller.start_cmd.assert_not_awaited()


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "result_enum, expected_text",
    [
        (
            UserRegistrationResult.REGISTER_USER_SUCCESS,
            "Welcome Marko, \nnow you are registered user",
        ),
        (UserRegistrationResult.REGISTERED_USER, "Welcome back Marko"),
    ],
)
async def test_start_when_from_user_is_new_user(
    mock_message_factory, mock_user, mock_user_controller, result_enum, expected_text
):

    mock_message = mock_message_factory(from_user=mock_user)

    mock_user_controller.start_cmd.return_value = UserDomain(
        msg=result_enum,
        id=mock_user.id,
        telegram_id=mock_user.telegram_id,
        name=mock_user.first_name,
    )

    await start(mock_message, mock_user_controller)

    mock_message.answer.assert_awaited_once_with(expected_text)
    mock_user_controller.start_cmd.assert_awaited_once_with(
        RequestUserDomain(mock_user.id, mock_user.first_name)
    )
