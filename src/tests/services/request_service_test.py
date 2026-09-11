from datetime import datetime
from decimal import Decimal

import pytest

from shopping_bot.core.domains.product_domain import ResponseProductDomain
from shopping_bot.core.domains.request_domain import (
    RequestInputResult,
    ResponseRequestDomain,
    ResultRequestDomain,
)
from shopping_bot.core.domains.user_domain import ResponseUserDomain
from shopping_bot.core.records.product_records import ResponseProductRecord
from shopping_bot.core.records.request_records import ResponseRequestRecord
from shopping_bot.core.records.user_records import ResponseUserRecord
from shopping_bot.core.records.utils import RequestStatus
from shopping_bot.services.request_service import RequestService


@pytest.mark.parametrize(
    "quantity, result",
    [
        ("10", RequestInputResult.QUANTITY_ACCEPTED),
        (None, RequestInputResult.INVALID_QUANTITY),
    ],
)
@pytest.mark.asyncio
async def test_process_quantity(
    mock_request_repository_factory,
    mock_user_controller,
    mock_user,
    mock_response,
    quantity,
    result,
):
    now = datetime.now()
    request_domain = ResponseRequestDomain(
        id=1,
        product_id=1,
        requested_by_user_id=1,
        requested_quantity=Decimal(quantity) if quantity is not None else Decimal(0),
        requested_at=now,
        product=ResponseProductDomain(id=1, name="milk", unit="l", description=None),
        requested_by_user=ResponseUserDomain(
            id=1,
            telegram_id=123,
            name="marko",
            is_admin=True,
            active_message_id=None,
            shopping_started_at=now,
            shopping_status=False,
        ),
    )
    expected = ResultRequestDomain(result, request_domain)

    result = ResultRequestDomain(result, request_domain)
    user = ResponseUserRecord(
        id=1,
        telegram_id=123,
        name="marko",
        is_admin=True,
        active_message_id=None,
        shopping_started_at=now,
        shopping_status=False,
    )
    request_record = ResponseRequestRecord(
        id=1,
        requested_quantity=Decimal(quantity) if quantity is not None else Decimal(0),
        requested_at=now,
        status=RequestStatus.pending,
        requested_by_user_id=1,
        product_id=1,
        receipt_id=None,
        price=None,
        quantity=None,
        match_confidence=None,
        product=ResponseProductRecord(id=1, name="milk", unit="l", description=None),
        requested_by_user=user,
    )

    request_record_list = [request_record, request_record]
    mock_repository = mock_request_repository_factory(
        request_record, request_record_list
    )
    mock_request_service = RequestService(mock_repository, mock_user_controller)
    result_request_domain = await mock_request_service.process_quantity(
        1, quantity if quantity is not None else " ", 123
    )
    assert result_request_domain.result == expected.result


@pytest.mark.asyncio
async def test_process_rquest_list(
    mock_request_repository_factory,
    mock_user_controller,
    mock_user,
    mock_response,
):
    now = datetime.now()

    user = ResponseUserRecord(
        id=1,
        telegram_id=123,
        name="marko",
        is_admin=True,
        active_message_id=None,
        shopping_started_at=now,
        shopping_status=False,
    )

    request_record = ResponseRequestRecord(
        id=1,
        requested_quantity=Decimal(10),
        requested_at=now,
        status=RequestStatus.pending,
        requested_by_user_id=1,
        product_id=1,
        receipt_id=None,
        price=None,
        quantity=None,
        match_confidence=None,
        product=ResponseProductRecord(id=1, name="milk", unit="l", description=None),
        requested_by_user=user,
    )

    request_record_list = [request_record, request_record]
    mock_repository = mock_request_repository_factory(
        request_record, request_record_list
    )
    mock_request_service = RequestService(mock_repository, mock_user_controller)
    result = await mock_request_service.process_request_list(
        RequestStatus.pending, RequestStatus.in_cart
    )
    assert len(result) == 2
