import pytest

from shopping_bot.core.domains.product_domain import (
    ProductInputResult,
    ResultProductDomain,
)
from shopping_bot.core.domains.utils import to_product_domain
from shopping_bot.core.records.product_records import ResponseProductRecord
from shopping_bot.services.product_service import ProductController


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "products_response, product_response, product_name, expected_value",
    [
        (
            [
                ResponseProductRecord(id=1, name="молоко", unit="l", description=None),
                ResponseProductRecord(
                    id=2, name="bread_with_butter", unit="u", description=None
                ),
            ],
            ResponseProductRecord(id=1, name="молоко", unit="l", description=None),
            "молоко",
            to_product_domain(
                ProductInputResult.PRODUCT_FOUND,
                ResponseProductRecord(id=1, name="молоко", unit="l", description=None),
            ),
        ),
        (
            [
                ResponseProductRecord(id=1, name="milk", unit="l", description=None),
                ResponseProductRecord(
                    id=2, name="bread_with_butter", unit="u", description=None
                ),
            ],
            ResponseProductRecord(
                id=1, name="bread_with_butter", unit="l", description=None
            ),
            "bread_witrouls_butter",
            to_product_domain(
                ProductInputResult.PRODUCT_NOT_FOUND_NEEDS_CONFIRMATION,
                ResponseProductRecord(
                    id=None, name="bread_with_butter", unit=None, description=None
                ),
            ),
        ),
        (
            [],
            ResponseProductRecord(id=1, name="milk", unit="l", description=None),
            "milk",
            to_product_domain(
                ProductInputResult.PRODUCT_CREATED,
                ResponseProductRecord(
                    id=None, name="milk", unit=None, description=None
                ),
            ),
        ),
    ],
)
async def test_process_product(
    mock_product_repository_factory,
    products_response,
    product_response,
    product_name,
    expected_value,
):

    mock_repository = mock_product_repository_factory(
        product_response, products_response
    )
    service = ProductController(mock_repository)
    res = await service.process_product(product_name=product_name)
    assert res == expected_value
