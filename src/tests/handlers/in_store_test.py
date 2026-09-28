from datetime import datetime
from decimal import Decimal
from unittest.mock import AsyncMock, MagicMock

import pytest

from shopping_bot.core.domains.request_domain import ResponseRequestDomain
from shopping_bot.core.records.utils import RequestStatus
from shopping_bot.handlers.in_store import (
    end_of_shopping,
    end_of_shopping_without_receipt,
    in_store,
    request_in_cart_and_back,
)
from shopping_bot.keyboards.in_store_kbd import get_inline_product_list_keyboard
from shopping_bot.keyboards.main_kbd import get_cancel_keyboard, get_main_keyboard
from shopping_bot.states.user_states import WaitFor


@pytest.mark.asyncio
async def test_in_store(
    mock_message_factory, mock_request_controller, mock_user, mock_response
):
    mock_message = mock_message_factory(from_user=mock_user, text=" ")
    now = datetime.now()

    mock_response = [
        ResponseRequestDomain(
            id=1,
            product_id=1,
            requested_by_user_id=1,
            requested_quantity=Decimal(10),
            quantity=Decimal(0),
            price=Decimal(0),
            requested_at=now,
            status=RequestStatus.pending,
            requested_by_user=mock_user,
            product=mock_response,
        ),
        ResponseRequestDomain(
            id=2,
            product_id=2,
            requested_by_user_id=1,
            quantity=Decimal(0),
            price=Decimal(0),
            requested_quantity=Decimal(15),
            requested_at=now,
            status=RequestStatus.pending,
            requested_by_user=mock_user,
            product=mock_response,
        ),
    ]

    mock_request_controller.process_request_list.return_value = mock_response

    await in_store(mock_message, mock_request_controller)
    mock_request_controller.process_request_list.assert_awaited_once_with(
        RequestStatus.in_cart, RequestStatus.pending
    )

    mock_message.answer.assert_awaited_once_with(
        "Список покупок:",
        reply_markup=get_inline_product_list_keyboard(mock_response),
    )


@pytest.mark.asyncio
async def test_request_in_cart_and_back(
    mock_callback_query, mock_request_controller, mock_user, mock_response, mock_state
):
    now = datetime.now()
    request_domain_list = [
        ResponseRequestDomain(
            id=1,
            product_id=1,
            requested_by_user_id=1,
            requested_quantity=Decimal(10),
            requested_at=now,
            quantity=Decimal(0),
            price=Decimal(0),
            status=RequestStatus.pending,
            requested_by_user=mock_user,
            product=mock_response,
        ),
        ResponseRequestDomain(
            id=2,
            product_id=2,
            requested_by_user_id=2,
            requested_quantity=Decimal(15),
            quantity=Decimal(0),
            price=Decimal(0),
            requested_at=now,
            status=RequestStatus.pending,
            requested_by_user=mock_user,
            product=mock_response,
        ),
    ]
    mock_request_controller.process_request_list.return_value = request_domain_list
    await request_in_cart_and_back(
        mock_callback_query, mock_state, mock_request_controller
    )
    mock_callback_query.answer.assert_awaited_once()
    mock_request_controller.process_request_in_cart_and_back.assert_awaited_once_with(
        int(mock_callback_query.data.split("_")[1])
    )
    mock_callback_query.message.edit_reply_markup.assert_awaited_once()


@pytest.mark.parametrize("data", [None, "cart_abc"])
@pytest.mark.asyncio
async def test_request_in_cart_and_back_invalid_data(
    mock_callback_query, mock_request_controller, mock_state, data
):
    mock_callback_query.data = data

    with pytest.raises(ValueError):
        await request_in_cart_and_back(
            mock_callback_query, mock_state, mock_request_controller
        )

    mock_callback_query.answer.assert_awaited_once()
    mock_request_controller.process_request_in_cart_and_back.assert_not_awaited()


@pytest.mark.asyncio
async def test_end_of_shopping(
    mock_callback_query, mock_request_controller, mock_state
):
    mock_callback_query.message.answer = AsyncMock()
    mock_request_controller.process_request_list.return_value = ["request"]

    await end_of_shopping(mock_callback_query, mock_state, mock_request_controller)

    mock_request_controller.process_request_list.assert_awaited_once_with(
        RequestStatus.in_cart
    )
    mock_state.update_data.assert_awaited_once_with(request_domain_list=["request"])
    mock_callback_query.message.answer.assert_awaited_once()
    assert mock_callback_query.message.answer.await_args.kwargs[
        "reply_markup"
    ] == get_cancel_keyboard("Без чека")
    mock_state.set_state.assert_awaited_once_with(WaitFor.receipt)
    mock_callback_query.answer.assert_awaited_once()


@pytest.mark.asyncio
async def test_end_of_shopping_without_message(
    mock_callback_query, mock_request_controller, mock_state
):
    mock_callback_query.message = None

    await end_of_shopping(mock_callback_query, mock_state, mock_request_controller)

    mock_state.set_state.assert_awaited_once_with(WaitFor.receipt)


@pytest.mark.asyncio
async def test_end_of_shopping_without_receipt(
    mock_message_factory, mock_user, mock_state
):
    message = mock_message_factory(from_user=mock_user, text="Без чека")
    mock_state.get_value = AsyncMock(return_value=["request"])
    receipt_controller = MagicMock()
    receipt_controller.process_empty_receipt = AsyncMock()

    await end_of_shopping_without_receipt(message, mock_state, receipt_controller)

    receipt_controller.process_empty_receipt.assert_awaited_once_with(
        mock_user.id, ["request"]
    )
    mock_state.clear.assert_awaited_once()
    message.answer.assert_awaited_once_with(
        "Покупка закрыта без чека", reply_markup=get_main_keyboard()
    )


@pytest.mark.asyncio
async def test_end_of_shopping_without_receipt_no_requests(
    mock_message_factory, mock_user, mock_state
):
    message = mock_message_factory(from_user=mock_user, text="Без чека")
    mock_state.get_value = AsyncMock(return_value=None)

    with pytest.raises(ValueError):
        await end_of_shopping_without_receipt(message, mock_state, MagicMock())
