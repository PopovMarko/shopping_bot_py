from unittest.mock import call

import pytest
from aiogram.types import ReplyKeyboardMarkup

from shopping_bot.core.domains.product_domain import ProductInputResult
from shopping_bot.core.domains.request_domain import RequestInputResult
from shopping_bot.handlers.utils import parse_product_response, parse_request_response
from shopping_bot.keyboards.add_product_kbd import (
    PRODUCT_CONFIRM_KBD,
)
from shopping_bot.states.user_states import WaitFor


@pytest.mark.parametrize(
    "input_result",
    [
        (ProductInputResult.PRODUCT_FOUND),
        (ProductInputResult.PRODUCT_NOT_FOUND_NEEDS_CONFIRMATION),
        (ProductInputResult.PRODUCT_CREATED),
        (RequestInputResult.QUANTITY_ACCEPTED),
        (RequestInputResult.INVALID_QUANTITY),
    ],
)
@pytest.mark.asyncio
async def test_parse_product_response(
    mock_message_factory,
    mock_state,
    mock_response,
    mock_user,
    input_result,
):
    mock_message = mock_message_factory(mock_user)
    mock_response.result = input_result

    if input_result in [
        ProductInputResult.PRODUCT_FOUND,
        ProductInputResult.PRODUCT_NOT_FOUND_NEEDS_CONFIRMATION,
        ProductInputResult.PRODUCT_CREATED,
    ]:
        await parse_product_response(mock_message, mock_state, mock_response)
    else:
        await parse_request_response(mock_message, mock_state, mock_response)

    match input_result:
        case ProductInputResult.PRODUCT_FOUND:
            calls = [
                call(product_id=mock_response.product_id),
                call(product_name=mock_response.product_name),
            ]
            mock_state.update_data.assert_has_awaits(calls, any_order=False)
            mock_state.set_state.assert_awaited_once_with(WaitFor.quantity)
            mock_message.answer.assert_awaited_once_with(
                f"Enter quantity for {mock_response.product_name}"
            )
        case ProductInputResult.PRODUCT_NOT_FOUND_NEEDS_CONFIRMATION:
            mock_state.update_data.assert_awaited_once_with(
                suggested_product_id=mock_response.product_id
            )
            mock_state.set_state.assert_awaited_once_with(WaitFor.confirmation)
            mock_message.answer.assert_awaited_once_with(
                f"You mean {mock_response.product_name}?",
                reply_markup=ReplyKeyboardMarkup(
                    keyboard=PRODUCT_CONFIRM_KBD, resize_keyboard=True
                ),
            )
        case ProductInputResult.PRODUCT_CREATED:
            mock_state.set_state.assert_awaited_once_with(WaitFor.unit)
            mock_message.answer.assert_awaited_once_with(
                f"Choose units for {mock_response.product_name}"
            )
        case RequestInputResult.QUANTITY_ACCEPTED:
            mock_state.set_state.assert_awaited_once_with(WaitFor.product)
            mock_message.answer.assert_awaited_once_with(
                "Enter next product or empty message to quit"
            )
        case RequestInputResult.INVALID_QUANTITY:
            mock_message.answer.assert_awaited_once_with("Enter correct quantity")
