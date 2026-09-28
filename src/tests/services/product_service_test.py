from unittest.mock import AsyncMock

import pytest

from shopping_bot.core.domains.product_domain import (
    InputProductDomain,
    ProductInputResult,
    ResponseProductDomain,
)
from shopping_bot.core.records.product_records import ResponseProductRecord
from shopping_bot.services.product_service import ProductController
from shopping_bot.services.utils import Product


@pytest.mark.parametrize(
    "product_input, expected",
    [
        ("milk", ProductInputResult.PRODUCT_FOUND),
        ("Milk", ProductInputResult.PRODUCT_NOT_FOUND_NEEDS_CONFIRMATION),
        ("beer", ProductInputResult.PRODUCT_CREATED),
    ],
)
@pytest.mark.asyncio
async def test_process_product(
    mock_product_repository_factory, product_input, expected
):
    product_response = ResponseProductRecord(
        name="milk",
        id=1,
        unit="l",
        description=None,
    )
    products_response = [product_response]
    mock_repository = mock_product_repository_factory(
        product_response, products_response
    )
    product_controller = ProductController(mock_repository)
    result = await product_controller.process_product(product_input)
    print(result.result)
    print(expected)
    assert result.result == expected
    mock_repository.get_products.assert_awaited_once()


@pytest.mark.parametrize(
    "confirmed, product_id, product_name, expected",
    [
        (True, 1, "milk", ProductInputResult.PRODUCT_FOUND),
        (False, 1, "beer", ProductInputResult.PRODUCT_CREATED),
    ],
)
@pytest.mark.asyncio
async def test_process_confirmation(
    mock_product_repository_factory, confirmed, product_id, product_name, expected
):
    product_response = ResponseProductRecord(
        name="milk",
        id=1,
        unit="l",
        description=None,
    )
    products_response = [product_response]
    mock_repository = mock_product_repository_factory(
        product_response, products_response
    )
    product_controller = ProductController(mock_repository)
    result = await product_controller.process_confirmation(
        confirmed, product_id, product_name
    )
    assert result.result == expected
    if confirmed:
        mock_repository.get_product.assert_awaited_once_with(product_id)


@pytest.mark.asyncio
async def test_process_unit(mock_product_repository_factory):
    product_response = ResponseProductRecord(
        name="milk",
        id=1,
        unit="l",
        description=None,
    )
    products_response = [product_response]
    mock_repository = mock_product_repository_factory(
        product_response, products_response
    )
    product_controller = ProductController(mock_repository)
    result = await product_controller.process_unit(unit_str="l", name="milk")
    assert result.result == ProductInputResult.UNIT_ACCEPTED
    mock_repository.create_product.assert_awaited_once_with(
        InputProductDomain("milk", "l", None)
    )


@pytest.mark.asyncio
async def test_process_product_without_name(mock_product_repository_factory):
    mock_repository = mock_product_repository_factory(
        ResponseProductRecord(id=1, name="milk", unit="l"), []
    )

    with pytest.raises(ValueError):
        await ProductController(mock_repository).process_product("")


@pytest.mark.parametrize(
    "confirmed, product_id, product_name",
    [(True, None, "milk"), (False, 1, None)],
)
@pytest.mark.asyncio
async def test_process_confirmation_missing_value(
    mock_product_repository_factory, confirmed, product_id, product_name
):
    mock_repository = mock_product_repository_factory(
        ResponseProductRecord(id=1, name="milk", unit="l"), []
    )

    with pytest.raises(ValueError):
        await ProductController(mock_repository).process_confirmation(
            confirmed, product_id, product_name
        )


@pytest.mark.asyncio
async def test_process_unit_without_unit(mock_product_repository_factory):
    mock_repository = mock_product_repository_factory(
        ResponseProductRecord(id=1, name="milk", unit="l"), []
    )

    with pytest.raises(ValueError):
        await ProductController(mock_repository).process_unit(None, "milk")  # type: ignore[arg-type]


@pytest.mark.parametrize("similar_found", [True, False])
@pytest.mark.asyncio
async def test_process_product_from_receipt(
    mock_product_repository_factory, similar_found
):
    record = ResponseProductRecord(id=1, name="milk", unit="l")
    mock_repository = mock_product_repository_factory(record, [])
    mock_repository.get_similar_product = AsyncMock(
        return_value=record if similar_found else None
    )

    res = await ProductController(mock_repository).process_product_from_receipt(
        Product(name="milk", price=None, quantity=None, unit="l", match_confidence=None)
    )

    assert res == ResponseProductDomain(id=1, name="milk", unit="l")
    if similar_found:
        mock_repository.create_product.assert_not_awaited()
    else:
        mock_repository.create_product.assert_awaited_once()
