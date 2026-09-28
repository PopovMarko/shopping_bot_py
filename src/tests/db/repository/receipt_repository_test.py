from datetime import datetime
from decimal import Decimal
from unittest.mock import MagicMock, patch

import pytest

from shopping_bot.core.records.request_records import (
    ResponseReceiptRecord,
    ResponseStoreRecord,
)
from shopping_bot.core.records.utils import RequestStatus
from shopping_bot.db.repository.receipt_repository import ReceiptRepository
from shopping_bot.services.utils import ModelResponse, Product, Store

FACTORY_PATH = "shopping_bot.db.repository.receipt_repository.async_session_factory"
NOW = datetime(2026, 9, 28, 12, 0)


def _store_model():
    model = MagicMock(id=1, address="Warszawa, Marszałkowska")
    model.name = "Lidl"
    return model


@pytest.mark.asyncio
async def test_create_receipt(mock_async_session_factory):
    factory, session = mock_async_session_factory
    receipt_model = MagicMock(
        id=10,
        store_id=1,
        uploaded_by_user_id=1,
        receipt_date=NOW,
        image_url=None,
        raw_model_response=None,
        created_at=NOW,
    )
    result = MagicMock()
    result.scalar_one.return_value = receipt_model
    session.execute.return_value = result

    receipt = ModelResponse(
        store=Store(id=1, name="Lidl", address="Warszawa"),
        receipt_date=NOW,
        total_amount=Decimal("3.00"),
        product=[
            Product(
                id=5,
                name="milk",
                price=Decimal("1.50"),
                quantity=Decimal(2),
                unit="l",
                match_confidence=90,
            )
        ],
        uploaded_by_user_id=1,
    )

    with patch(FACTORY_PATH, factory):
        res = await ReceiptRepository().create_receipt(receipt)

    assert res == ResponseReceiptRecord(
        id=10,
        store_id=1,
        uploaded_by_user_id=1,
        receipt_date=NOW,
        image_url=None,
        raw_model_response=None,
        created_at=NOW,
    )
    update_rows = session.execute.await_args_list[1].args[1]
    assert update_rows == [
        {
            "id": 5,
            "receipt_id": 10,
            "price": Decimal("1.50"),
            "quantity": Decimal(2),
            "match_confidence": 90,
            "status": RequestStatus.fulfilled,
        }
    ]
    session.commit.assert_awaited_once()


@pytest.mark.asyncio
async def test_get_product_name_list(mock_async_session_factory):
    factory, session = mock_async_session_factory
    result = MagicMock()
    result.scalars.return_value.all.return_value = ["milk", "bread"]
    session.execute.return_value = result

    with patch(FACTORY_PATH, factory):
        res = await ReceiptRepository().get_product_name_list([1, 2])

    assert res == ["milk", "bread"]


@pytest.mark.asyncio
async def test_get_store_by_name_and_address(mock_async_session_factory):
    factory, session = mock_async_session_factory
    result = MagicMock()
    result.scalar_one_or_none.return_value = _store_model()
    session.execute.return_value = result

    with patch(FACTORY_PATH, factory):
        res = await ReceiptRepository().get_store_by_name_and_address(
            "Lidl", "Warszawa, Marszałkowska"
        )

    assert res == ResponseStoreRecord(
        id=1, name="Lidl", address="Warszawa, Marszałkowska"
    )


@pytest.mark.asyncio
async def test_get_store_by_name_and_address_not_found(mock_async_session_factory):
    factory, session = mock_async_session_factory
    result = MagicMock()
    result.scalar_one_or_none.return_value = None
    session.execute.return_value = result

    with patch(FACTORY_PATH, factory):
        res = await ReceiptRepository().get_store_by_name_and_address("Lidl", None)

    assert res is None


@pytest.mark.parametrize("address", ["Warszawa, Marszałkowska", None])
@pytest.mark.asyncio
async def test_create_store(mock_async_session_factory, address):
    factory, session = mock_async_session_factory
    result = MagicMock()
    result.scalar_one.return_value = _store_model()
    session.execute.return_value = result

    with patch(FACTORY_PATH, factory):
        res = await ReceiptRepository().create_store("Lidl", address)

    assert res.name == "Lidl"
    session.commit.assert_awaited_once()


@pytest.mark.asyncio
async def test_create_store_without_name():
    with pytest.raises(ValueError):
        await ReceiptRepository().create_store(None, "Warszawa")


@pytest.mark.asyncio
async def test_update_receipt():
    assert await ReceiptRepository().update_receipt() is None
