from datetime import datetime
from decimal import Decimal
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from shopping_bot.core.domains.history_domain import StatisticsRequest
from shopping_bot.core.domains.product_domain import ResponseProductDomain
from shopping_bot.core.domains.receipt_domain import ResponseReceiptDomain
from shopping_bot.core.domains.user_domain import InputUserDomain
from shopping_bot.core.domains.utils import (
    product_record_to_domain,
    statistics_shopping_record_to_domain,
    to_response_product_domain,
    to_response_receipt_domain,
    user_record_to_input_domain,
)
from shopping_bot.core.interfaces.service.in_store_controller_interface import (
    InStoreControllerInterface,
)
from shopping_bot.core.logger import configure_logger
from shopping_bot.core.middleware import TimingMiddleware
from shopping_bot.core.records.history_records import StatisticsRequestRecord
from shopping_bot.core.records.product_records import ResponseProductRecord
from shopping_bot.core.records.request_records import ResponseReceiptRecord
from shopping_bot.core.records.user_records import ResponseUserRecord
from shopping_bot.db.postgres import engine

NOW = datetime(2026, 9, 28, 12, 0)


@pytest.mark.asyncio
async def test_timing_middleware():
    handler = AsyncMock(return_value="result")

    res = await TimingMiddleware()(handler, "event", {"key": "value"})

    assert res == "result"
    handler.assert_awaited_once_with("event", {"key": "value"})


def test_configure_logger():
    with patch("shopping_bot.core.logger.logging.basicConfig") as basic_config:
        configure_logger("WARNING")

    assert basic_config.call_args.kwargs["level"] == "WARNING"


def test_in_store_controller_interface_is_protocol():
    assert hasattr(InStoreControllerInterface, "process_in_store")


def test_get_engine(monkeypatch):
    monkeypatch.setenv("DATABASE_URL", "postgresql+asyncpg://u:p@host/db")
    engine.get_engine.cache_clear()
    with patch.object(engine, "create_async_engine") as create_engine:
        res = engine.get_engine()
    engine.get_engine.cache_clear()

    create_engine.assert_called_once_with("postgresql+asyncpg://u:p@host/db", echo=True)
    assert res is create_engine.return_value


def test_async_session_factory():
    with (
        patch.object(engine, "get_engine") as get_engine,
        patch.object(engine, "async_sessionmaker") as sessionmaker,
    ):
        res = engine.async_session_factory()

    sessionmaker.assert_called_once_with(
        bind=get_engine.return_value, expire_on_commit=False
    )
    assert res is sessionmaker.return_value.return_value


def test_product_record_to_domain():
    record = ResponseProductRecord(id=1, name="milk", unit="l", description="d")
    assert product_record_to_domain(record) == ResponseProductDomain(
        id=1, name="milk", unit="l", description="d"
    )


def test_to_response_product_domain_without_unit():
    with pytest.raises(ValueError):
        to_response_product_domain(ResponseProductRecord(id=1, name="milk"))


def test_user_record_to_input_domain():
    record = ResponseUserRecord(
        id=1,
        telegram_id=123,
        name="Marko",
        is_admin=True,
        shopping_status=False,
        active_message_id=None,
        shopping_started_at=None,
    )
    assert user_record_to_input_domain(record) == InputUserDomain(
        telegram_id=123, name="Marko", is_admin=True
    )


def test_to_response_receipt_domain():
    record = ResponseReceiptRecord(
        id=1,
        store_id=2,
        uploaded_by_user_id=3,
        receipt_date=NOW,
        image_url=None,
        raw_model_response=None,
        created_at=NOW,
    )
    assert to_response_receipt_domain(record) == ResponseReceiptDomain(
        id=1,
        store_id=2,
        uploaded_by_user_id=3,
        receipt_date=NOW,
        image_url=None,
        raw_model_response=None,
        created_at=NOW,
    )


def test_statistics_shopping_record_to_domain():
    records = [StatisticsRequestRecord("milk", Decimal(2), Decimal("3.00"))]
    assert statistics_shopping_record_to_domain(records) == [
        StatisticsRequest("milk", Decimal(2), Decimal("3.00"))
    ]


def test_receipt_model_to_record_without_date():
    from shopping_bot.db.repository.utils import receipt_model_to_record

    model = MagicMock(
        id=1,
        store_id=None,
        uploaded_by_user_id=1,
        receipt_date=None,
        image_url=None,
        raw_model_response=None,
        created_at=NOW,
    )
    before = datetime.now()
    assert receipt_model_to_record(model).receipt_date >= before
