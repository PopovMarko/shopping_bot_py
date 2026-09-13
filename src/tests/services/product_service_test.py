import pytest

from shopping_bot.core.domains.product_domain import (
    InputProductDomain,
    ProductInputResult,
)
from shopping_bot.core.records.product_records import ResponseProductRecord
from shopping_bot.services.product_service import ProductController


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
