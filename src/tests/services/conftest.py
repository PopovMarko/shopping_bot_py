from unittest.mock import AsyncMock, MagicMock

import pytest

from shopping_bot.core.records.product_records import ResponseProductRecord
from shopping_bot.core.records.user_records import ResponseUserRecord


@pytest.fixture
def mock_user_repository_factory():
    def _make(
        save_user_response: ResponseUserRecord,
        user_record: ResponseUserRecord | None = None,
    ):
        repository = MagicMock()
        repository.get_user_by_telegram_id = AsyncMock()
        repository.get_user_by_telegram_id.return_value = user_record
        repository.save_user = AsyncMock()
        repository.save_user.return_value = save_user_response
        return repository

    return _make


@pytest.fixture
def mock_product_repository_factory():
    def _make(
        product_response: ResponseProductRecord,
        products_response: list[ResponseProductRecord],
    ):
        repository = MagicMock()
        repository.get_products = AsyncMock()
        repository.get_uproducts.return_value = products_response

        repository.get_product = AsyncMock()
        repository.get_product.return_value = product_response

        repository.create_product = AsyncMock()
        repository.create_product.return_value = product_response
        return repository

    return _make
