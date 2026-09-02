from datetime import datetime
from decimal import Decimal

import pytest

from shopping_bot.core.domains.request_domain import (
    RequestInputResult,
    ResultRequestDomain,
)
from shopping_bot.core.records.request_records import ResponseRequestRecord
from shopping_bot.core.records.utils import RequestStatus
from shopping_bot.services.request_service import RequestService


@pytest.mark.parametrize(
    "product_id, quantity, telegram_user_id, result",
    [
        (1, "10", 123, RequestInputResult.QUANTITY_ACCEPTED),
        (1, "invalid", 123, RequestInputResult.INVALID_QUANTITY),
    ],
)
@pytest.mark.asyncio
async def test_process_quantity(
    mock_request_repository_factory,
    mock_user_controller,
    mock_user,
    mock_response,
    product_id,
    quantity,
    telegram_user_id,
    result,
):
    now = datetime.now()
    result = ResultRequestDomain(
        result, mock_response, mock_user, 1, quantity, now, RequestStatus.pending
    )
    request_record = ResponseRequestRecord(
        id=1,
        requested_quantity=Decimal(10),
        requested_at=now,
        status=RequestStatus.pending,
        user=mock_user,
        product=mock_response,
    )

    request_record_list = [request_record, request_record]
    mock_repository = mock_request_repository_factory(
        request_record, request_record_list
    )
    mock_request_service = RequestService(mock_repository, mock_user_controller)
    result_request_domain = await mock_request_service.process_quantity(
        product_id, quantity, telegram_user_id
    )
    assert result_request_domain.result == result.result


@pytest.mark.asyncio
async def test_process_rquest_list(
    mock_request_repository_factory,
    mock_user_controller,
    mock_user,
    mock_response,
):
    now = datetime.now()
    request_record = ResponseRequestRecord(
        id=1,
        requested_quantity=Decimal(10),
        requested_at=now,
        status=RequestStatus.pending,
        user=mock_user,
        product=mock_response,
    )

    request_record_list = [request_record, request_record]
    mock_repository = mock_request_repository_factory(
        request_record, request_record_list
    )
    mock_request_service = RequestService(mock_repository, mock_user_controller)
    result = await mock_request_service.process_request_list(
        RequestStatus.pending, RequestStatus.in_cart
    )
