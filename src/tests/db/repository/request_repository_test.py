from datetime import datetime
from decimal import Decimal
from unittest.mock import MagicMock, patch

import pytest

from shopping_bot.core.domains.request_domain import InputRequestDomain
from shopping_bot.core.records.product_records import ResponseProductRecord
from shopping_bot.core.records.request_records import ResponseRequestRecord
from shopping_bot.core.records.user_records import ResponseUserRecord
from shopping_bot.core.records.utils import RequestStatus
from shopping_bot.db.repository.request_repository import RequestRepository

FACTORY_PATH = "shopping_bot.db.repository.request_repository.async_session_factory"
NOW = datetime(2026, 9, 28, 12, 0)


def _request_model():
    product = MagicMock(id=1, unit="l", description=None)
    product.name = "milk"
    user = MagicMock(
        id=1,
        telegram_id=123,
        is_admin=False,
        shopping_status=False,
        active_message_id=None,
        shopping_started_at=None,
    )
    user.name = "Marko"
    return MagicMock(
        id=1,
        product_id=1,
        requested_by_user_id=1,
        requested_quantity=Decimal(2),
        requested_at=NOW,
        receipt_id=None,
        price=None,
        quantity=None,
        match_confidence=None,
        status=RequestStatus.pending,
        product=product,
        requested_by_user=user,
    )


EXPECTED = ResponseRequestRecord(
    id=1,
    requested_quantity=Decimal(2),
    requested_at=NOW,
    status=RequestStatus.pending,
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
        name="Marko",
        is_admin=False,
        shopping_status=False,
        active_message_id=None,
        shopping_started_at=None,
    ),
)


@pytest.mark.asyncio
async def test_create_request(mock_async_session_factory):
    factory, session = mock_async_session_factory
    result = MagicMock()
    result.scalar_one.return_value = _request_model()
    session.execute.return_value = result

    with patch(FACTORY_PATH, factory):
        res = await RequestRepository().create_request(
            InputRequestDomain(
                product_id=1,
                requested_by_user_id=1,
                requested_quantity=Decimal(2),
                requested_at=NOW,
                quantity=None,
                price=None,
                status=RequestStatus.pending,
            )
        )

    assert res == EXPECTED
    session.commit.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_request_list(mock_async_session_factory):
    factory, session = mock_async_session_factory
    result = MagicMock()
    result.scalars.return_value = [_request_model(), _request_model()]
    session.execute.return_value = result

    with patch(FACTORY_PATH, factory):
        res = await RequestRepository().get_request_list(
            RequestStatus.pending, RequestStatus.in_cart
        )

    assert res == [EXPECTED, EXPECTED]


@pytest.mark.asyncio
async def test_get_request_by_id(mock_async_session_factory):
    factory, session = mock_async_session_factory
    result = MagicMock()
    result.scalar_one.return_value = _request_model()
    session.execute.return_value = result

    with patch(FACTORY_PATH, factory):
        res = await RequestRepository().get_request_by_id(1)

    assert res == EXPECTED


@pytest.mark.asyncio
async def test_update_request_status(mock_async_session_factory):
    factory, session = mock_async_session_factory

    with patch(FACTORY_PATH, factory):
        res = await RequestRepository().update_request_status(1, RequestStatus.in_cart)

    assert res is None
    session.execute.assert_awaited_once()
    session.commit.assert_awaited_once()
