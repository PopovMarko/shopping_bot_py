from datetime import datetime
from decimal import Decimal

import pytest

from shopping_bot.core.domains.request_domain import (
    RequestInputResult,
)
from shopping_bot.core.records.request_records import ResponseRequestRecord
from shopping_bot.services.request_service import RequestService
from tests.handlers.conftest import mock_user_controller


@pytest.mark.parametrize(
    "product_id, quantity_str, telegram_id, status",
    [
        (
            1,
            "10",
            123,
            RequestInputResult.QUANTITY_ACCEPTED,
        ),
        (1, "10x", 123, RequestInputResult.INVALID_QUANTITY),
    ],
)
@pytest.mark.asyncio
async def test_process_quantity(
    product_id,
    quantity_str,
    telegram_id,
    mock_request_repository_factory,
    mock_user,
    mock_response,
    status,
):

    now = datetime.now()

    mock_repository = mock_request_repository_factory(
        request_record=ResponseRequestRecord(
            id=1,
            requested_quantity=Decimal(10),
            requested_at=now,
            user=mock_user,
            product=mock_response,
            status=status,
        )
    )

    mock_user_controller.get_user_id_by_telegram_id.return_value = mock_user
    request_service = RequestService(
        repository=mock_repository, user_service=mock_user_controller
    )

    res = await request_service.process_quantity(product_id, quantity_str, telegram_id)
    print(res)
    # assert res == expected
