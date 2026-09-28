from unittest.mock import MagicMock, patch

import pytest

from shopping_bot.core.domains.product_domain import InputProductDomain
from shopping_bot.core.records.product_records import ResponseProductRecord
from shopping_bot.db.repository.product_repository import ProductRepository

FACTORY_PATH = "shopping_bot.db.repository.product_repository.async_session_factory"


def _product_model(id=1, name="milk", unit="l", description=None):
    model = MagicMock(id=id, unit=unit, description=description)
    model.name = name
    return model


@pytest.mark.asyncio
async def test_get_products(mock_async_session_factory):
    factory, session = mock_async_session_factory
    result = MagicMock()
    result.scalars.return_value = [
        _product_model(1, "milk", "l"),
        _product_model(2, "bread", "шт"),
    ]
    session.execute.return_value = result

    with patch(FACTORY_PATH, factory):
        res = await ProductRepository().get_products()

    assert res == [
        ResponseProductRecord(id=1, name="milk", unit="l", description=None),
        ResponseProductRecord(id=2, name="bread", unit="шт", description=None),
    ]


@pytest.mark.asyncio
async def test_get_products_none(mock_async_session_factory):
    factory, session = mock_async_session_factory
    result = MagicMock()
    result.scalars.return_value = None
    session.execute.return_value = result

    with patch(FACTORY_PATH, factory):
        res = await ProductRepository().get_products()

    assert res == []


@pytest.mark.asyncio
async def test_get_product(mock_async_session_factory):
    factory, session = mock_async_session_factory
    result = MagicMock()
    result.scalar_one.return_value = _product_model()
    session.execute.return_value = result

    with patch(FACTORY_PATH, factory):
        res = await ProductRepository().get_product(1)

    assert res == ResponseProductRecord(id=1, name="milk", unit="l")


@pytest.mark.asyncio
async def test_get_product_id_none():
    with pytest.raises(ValueError):
        await ProductRepository().get_product(None)  # type: ignore[arg-type]


@pytest.mark.asyncio
async def test_create_product(mock_async_session_factory):
    factory, session = mock_async_session_factory
    result = MagicMock()
    result.scalar_one.return_value = _product_model()
    session.execute.return_value = result

    with patch(FACTORY_PATH, factory):
        res = await ProductRepository().create_product(
            InputProductDomain(name="milk", unit="l")
        )

    assert res == ResponseProductRecord(id=1, name="milk", unit="l")
    session.commit.assert_awaited_once()


@pytest.mark.asyncio
async def test_create_product_none():
    with pytest.raises(ValueError):
        await ProductRepository().create_product(None)  # type: ignore[arg-type]


@pytest.mark.asyncio
async def test_get_similar_product(mock_async_session_factory):
    factory, session = mock_async_session_factory
    result = MagicMock()
    result.scalar_one_or_none.return_value = _product_model()
    session.execute.return_value = result

    with patch(FACTORY_PATH, factory):
        res = await ProductRepository().get_similar_product("milk")

    assert res == ResponseProductRecord(id=1, name="milk", unit="l")
    assert session.execute.await_count == 2


@pytest.mark.asyncio
async def test_get_similar_product_not_found(mock_async_session_factory):
    factory, session = mock_async_session_factory
    result = MagicMock()
    result.scalar_one_or_none.return_value = None
    session.execute.return_value = result

    with patch(FACTORY_PATH, factory):
        res = await ProductRepository().get_similar_product("milk")

    assert res is None
