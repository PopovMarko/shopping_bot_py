from datetime import datetime
from decimal import Decimal

import pytest

from shopping_bot.core.domains.request_domain import ResponseRequestDomain
from shopping_bot.core.records.utils import RequestStatus
from shopping_bot.handlers.add_quantity import add_quantity, request_list


@pytest.mark.parametrize(
    "text",
    ["10", None],
)
@pytest.mark.asyncio
async def test_process_add_quantity(
    mock_message_factory,
    mock_state,
    mock_request_controller,
    mock_user,
    mock_response,
    text,
):
    mock_message = mock_message_factory(from_user=mock_user, text=text)
    mock_state.get_value.side_effect = [
        mock_response.product_name,
        mock_response.product_id,
    ]

    await add_quantity(mock_message, mock_state, mock_request_controller)
    if mock_message.text is None:
        mock_message.answer.assert_awaited_once_with(
            f"Enter quantity of {mock_response.product_name}"
        )
    else:
        mock_request_controller.process_quantity.assert_awaited_once_with(
            mock_response.product_id, "10", 1
        )


@pytest.mark.asyncio
async def test_list_request(
    mock_message_factory, mock_request_controller, mock_user, mock_response
):
    mock_message = mock_message_factory(from_user=mock_user)
    now = datetime.now()
    res = [
        ResponseRequestDomain(
            id=1,
            requested_quantity=Decimal(10),
            requested_at=now,
            status=RequestStatus.pending,
            requested_by_user=mock_user,
            product=mock_response,
        ),
        ResponseRequestDomain(
            id=1,
            requested_quantity=Decimal(10),
            requested_at=now,
            status=RequestStatus.pending,
            requested_by_user=mock_user,
            product=mock_response,
        ),
    ]
    res_list = []
    for p in res:
        res_list.append(
            f"{p.requested_by_user.name} {p.product.name} {p.requested_quantity} {p.product.unit}"
        )
    res_str = "\n".join(res_list)

    mock_request_controller.process_request_list.return_value = res

    await request_list(mock_message, mock_request_controller)

    mock_request_controller.process_request_list.assert_awaited_once()
    mock_message.answer.assert_awaited_once_with(res_str)
