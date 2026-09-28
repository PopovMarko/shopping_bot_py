from datetime import datetime
from decimal import Decimal
from unittest.mock import MagicMock, patch

import pytest
from sqlalchemy.exc import NoResultFound

from shopping_bot.core.records.history_records import (
    LastShoppingRecord,
    StatisticsRequestRecord,
    lastShoppingProductRecord,
)
from shopping_bot.db.repository.history_repository import HistoryRepository

FACTORY_PATH = "shopping_bot.db.repository.history_repository.async_session_factory"


def _row(name, unit, quantity, price, receipt, user, store):
    request = MagicMock(quantity=quantity, price=price)
    product = MagicMock(unit=unit)
    product.name = name
    return (request, product, receipt, user, store)


@pytest.mark.asyncio
async def test_get_last_shopping(mock_async_session_factory):
    factory, session = mock_async_session_factory
    receipt_date = datetime(2026, 9, 28, 14, 35)
    receipt = MagicMock(receipt_date=receipt_date)
    user = MagicMock()
    user.name = "Marko"
    store = MagicMock()
    store.name = "Lidl"

    result = MagicMock()
    result.all.return_value = [
        _row("milk", "l", Decimal(2), Decimal("1.50"), receipt, user, store),
        _row("bread", None, Decimal(1), Decimal("3.00"), receipt, user, store),
    ]
    session.execute.return_value = result

    with patch(FACTORY_PATH, factory):
        res = await HistoryRepository().get_last_shopping(1)

    assert res == LastShoppingRecord(
        user_name="Marko",
        shopping_date=receipt_date,
        store_name="Lidl",
        products=[
            lastShoppingProductRecord("milk", "l", Decimal(2), Decimal("1.50")),
            lastShoppingProductRecord("bread", "", Decimal(1), Decimal("3.00")),
        ],
    )
    session.execute.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_last_shopping_orders_by_day_then_upload_time(
    mock_async_session_factory,
):
    factory, session = mock_async_session_factory
    result = MagicMock()
    result.all.return_value = [
        _row("milk", "l", Decimal(1), Decimal(1), MagicMock(), MagicMock(), None)
    ]
    session.execute.return_value = result

    with patch(FACTORY_PATH, factory):
        await HistoryRepository().get_last_shopping(1)

    sql = str(session.execute.await_args.args[0])
    assert "ORDER BY date(receipts.receipt_date) DESC NULLS LAST" in sql
    assert "receipts.created_at DESC, receipts.id DESC" in sql


@pytest.mark.asyncio
async def test_get_last_shopping_without_store(mock_async_session_factory):
    factory, session = mock_async_session_factory
    result = MagicMock()
    result.all.return_value = [
        _row("milk", "l", Decimal(1), Decimal(1), MagicMock(), MagicMock(), None)
    ]
    session.execute.return_value = result

    with patch(FACTORY_PATH, factory):
        res = await HistoryRepository().get_last_shopping(1)

    assert res.store_name == ""


@pytest.mark.asyncio
async def test_get_last_shopping_no_history(mock_async_session_factory):
    factory, session = mock_async_session_factory
    result = MagicMock()
    result.all.return_value = []
    session.execute.return_value = result

    with patch(FACTORY_PATH, factory), pytest.raises(NoResultFound):
        await HistoryRepository().get_last_shopping(1)


@pytest.mark.asyncio
async def test_get_statistics_shopping(mock_async_session_factory):
    factory, session = mock_async_session_factory
    result = MagicMock()
    result.all.return_value = [(1, "milk", Decimal("3.00"), Decimal(2))]
    session.execute.return_value = result

    with patch(FACTORY_PATH, factory):
        res = await HistoryRepository().get_statistics_shopping()

    assert res == [
        StatisticsRequestRecord(
            product_name="milk",
            product_quantity=Decimal("3.00"),
            product_cost=Decimal(2),
        )
    ]
