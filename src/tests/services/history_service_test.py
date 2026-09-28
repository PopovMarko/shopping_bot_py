from datetime import datetime
from decimal import Decimal
from unittest.mock import AsyncMock, MagicMock

import pytest

from shopping_bot.core.domains.history_domain import (
    LastShoppingDomain,
    LastShoppingRequestDomain,
    StatisticsRequest,
)
from shopping_bot.core.records.history_records import (
    LastShoppingRecord,
    StatisticsRequestRecord,
    lastShoppingProductRecord,
)
from shopping_bot.services.history_service import HistoryService

NOW = datetime(2026, 9, 28, 12, 0)


@pytest.fixture
def mock_history_repository():
    repository = MagicMock()
    repository.get_last_shopping = AsyncMock(
        return_value=LastShoppingRecord(
            user_name="Marko",
            shopping_date=NOW,
            store_name="Lidl",
            products=[
                lastShoppingProductRecord("milk", "l", Decimal(2), Decimal("1.50"))
            ],
        )
    )
    repository.get_statistics_shopping = AsyncMock(
        return_value=[StatisticsRequestRecord("milk", Decimal(2), Decimal("3.00"))]
    )
    return repository


@pytest.mark.asyncio
async def test_process_last_shopping(mock_history_repository, mock_user_controller):
    mock_user_controller.get_user_id_by_telegram_id.return_value = 1
    service = HistoryService(mock_history_repository, mock_user_controller)

    res = await service.process_last_shopping(123)

    assert res == LastShoppingDomain(
        user_name="Marko",
        last_shopping_date=NOW,
        store_name="Lidl",
        products=[LastShoppingRequestDomain("milk", "l", Decimal(2), Decimal("1.50"))],
    )
    mock_history_repository.get_last_shopping.assert_awaited_once_with(1)


@pytest.mark.asyncio
async def test_process_last_shopping_unknown_user(
    mock_history_repository, mock_user_controller
):
    mock_user_controller.get_user_id_by_telegram_id.return_value = None
    service = HistoryService(mock_history_repository, mock_user_controller)

    with pytest.raises(ValueError):
        await service.process_last_shopping(123)


@pytest.mark.asyncio
async def test_process_statistics_shopping(
    mock_history_repository, mock_user_controller
):
    service = HistoryService(mock_history_repository, mock_user_controller)

    res = await service.process_statistics_shopping()

    assert res == [StatisticsRequest("milk", Decimal(2), Decimal("3.00"))]
