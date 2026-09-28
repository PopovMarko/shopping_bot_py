from datetime import datetime
from decimal import Decimal
from unittest.mock import AsyncMock

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
        quantity=Decimal(0),
        price=Decimal(0),
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


def _request_record(status: RequestStatus) -> ResponseRequestRecord:
    return ResponseRequestRecord(
        id=1,
        requested_quantity=Decimal(1),
        requested_at=datetime(2026, 9, 28, 12, 0),
        status=status,
        requested_by_user_id=1,
        product_id=1,
        receipt_id=None,
        price=None,
        quantity=None,
        match_confidence=None,
        product=ResponseProductRecord(id=1, name="milk", unit="l", description=None),
        requested_by_user=ResponseUserRecord(
            id=1,
            telegram_id=123,
            name="marko",
            is_admin=False,
            active_message_id=None,
            shopping_started_at=None,
            shopping_status=False,
        ),
    )


@pytest.mark.parametrize(
    "current, new",
    [
        (RequestStatus.pending, RequestStatus.in_cart),
        (RequestStatus.in_cart, RequestStatus.pending),
        (RequestStatus.fulfilled, RequestStatus.cancelled),
    ],
)
@pytest.mark.asyncio
async def test_process_request_in_cart_and_back(
    mock_request_repository_factory, mock_user_controller, current, new
):
    record = _request_record(current)
    mock_repository = mock_request_repository_factory(record, [record])
    mock_repository.get_request_by_id = AsyncMock(return_value=record)
    mock_repository.update_request_status = AsyncMock()
    service = RequestService(mock_repository, mock_user_controller)

    res = await service.process_request_in_cart_and_back(1)

    mock_repository.update_request_status.assert_awaited_once_with(1, new)
    mock_repository.get_request_list.assert_awaited_once_with(
        RequestStatus.pending, RequestStatus.in_cart
    )
    assert [r.id for r in res] == [1]


@pytest.mark.parametrize("quantity", [Decimal(2), None])
@pytest.mark.asyncio
async def test_process_request_from_receipt(
    mock_request_repository_factory, mock_user_controller, quantity
):
    record = _request_record(RequestStatus.fulfilled)
    mock_repository = mock_request_repository_factory(record, [record])
    service = RequestService(mock_repository, mock_user_controller)

    res = await service.process_request_from_receipt(
        ResponseProductDomain(id=1, name="milk", unit="l"), 1, quantity
    )

    request = mock_repository.create_request.await_args.args[0]
    assert request.status == RequestStatus.fulfilled
    assert request.requested_quantity == (quantity or Decimal(0))
    assert res.id == 1


@pytest.mark.asyncio
async def test_process_quantity_unknown_user(
    mock_request_repository_factory, mock_user_controller
):
    record = _request_record(RequestStatus.pending)
    mock_repository = mock_request_repository_factory(record, [record])
    mock_user_controller.get_user_id_by_telegram_id.return_value = None
    service = RequestService(mock_repository, mock_user_controller)

    with pytest.raises(ValueError):
        await service.process_quantity(1, "2", 123)
