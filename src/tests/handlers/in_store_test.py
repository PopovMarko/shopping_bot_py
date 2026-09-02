from datetime import datetime
from decimal import Decimal

import pytest

from shopping_bot.core.domains.request_domain import ResponseRequestDomain
from shopping_bot.core.records.utils import RequestStatus
from shopping_bot.handlers.in_store import in_store, request_in_cart_and_back
from shopping_bot.keyboards.in_store_kbd import get_inline_product_list_keyboard


@pytest.mark.asyncio
async def test_in_store(
    mock_message_factory, mock_request_controller, mock_user, mock_response
):
    mock_message = mock_message_factory(from_user=mock_user, text=" ")
    now = datetime.now()

    mock_response = [
        ResponseRequestDomain(
            id=1,
            requested_quantity=Decimal(10),
            requested_at=now,
            status=RequestStatus.pending,
            requested_by_user=mock_user,
            product=mock_response,
        ),
        ResponseRequestDomain(
            id=2,
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
    mock_callback_query, mock_request_controller, mock_user, mock_response
):
    now = datetime.now()
    request_domain_list = [
        ResponseRequestDomain(
            id=1,
            requested_quantity=Decimal(10),
            requested_at=now,
            status=RequestStatus.pending,
            requested_by_user=mock_user,
            product=mock_response,
        ),
        ResponseRequestDomain(
            id=2,
            requested_quantity=Decimal(10),
            requested_at=now,
            status=RequestStatus.pending,
            requested_by_user=mock_user,
            product=mock_response,
        ),
    ]
    mock_request_controller.process_request_list.return_value = request_domain_list
    await request_in_cart_and_back(mock_callback_query, mock_request_controller)
    mock_callback_query.answer.assert_awaited_once()
    mock_request_controller.process_request_in_cart_and_back.assert_awaited_once_with(
        int(mock_callback_query.data.split("_")[1])
    )
    mock_callback_query.message.edit_reply_markup.assert_awaited_once()
