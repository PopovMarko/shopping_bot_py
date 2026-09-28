from datetime import datetime
from decimal import Decimal
from unittest.mock import AsyncMock, MagicMock

import httpx2
import pytest
from anthropic import APITimeoutError

from shopping_bot.core.domains.product_domain import ResponseProductDomain
from shopping_bot.core.domains.request_domain import ResponseRequestDomain
from shopping_bot.core.domains.user_domain import ResponseUserDomain
from shopping_bot.core.records.request_records import ResponseStoreRecord
from shopping_bot.core.records.user_records import ResponseUserRecord
from shopping_bot.services.receipt_service import ReceiptService
from shopping_bot.services.utils import ModelResponse

NOW = datetime(2026, 9, 28, 12, 0)

USER_RECORD = ResponseUserRecord(
    id=1,
    telegram_id=123,
    name="Marko",
    is_admin=False,
    shopping_status=False,
    active_message_id=None,
    shopping_started_at=None,
)


def _request_domain(
    id: int, name: str, product_id: int | None = None
) -> ResponseRequestDomain:
    return ResponseRequestDomain(
        id=id,
        product_id=product_id if product_id is not None else id,
        requested_by_user_id=1,
        requested_quantity=Decimal(1),
        requested_at=NOW,
        quantity=Decimal(1),
        price=None,
        product=ResponseProductDomain(id=id, name=name, unit="l"),
        requested_by_user=ResponseUserDomain(
            id=1,
            telegram_id=123,
            name="Marko",
            is_admin=False,
            shopping_status=False,
            active_message_id=None,
            shopping_started_at=None,
        ),
    )


def _llm_response(
    receipt_date: str, product_names: tuple[str, ...] = ("milk", "bread")
) -> MagicMock:
    block = MagicMock(type="tool_use")
    block.input = {
        "store": {"name": "Lidl", "address": "Warszawa"},
        "receipt_date": receipt_date,
        "total_amount": "5.50",
        "product": [
            {
                "name": name,
                "price": "1.50",
                "quantity": "1",
                "unit": "l",
                "match_confidence": "90",
            }
            for name in product_names
        ],
    }
    response = MagicMock()
    response.content = [MagicMock(type="text"), block]
    return response


@pytest.fixture
def receipt_service_factory():
    def _make(store_record: ResponseStoreRecord | None = None, user_record=USER_RECORD):
        repository = MagicMock()
        repository.get_product_name_list = AsyncMock(return_value=["milk"])
        repository.get_store_by_name_and_address = AsyncMock(return_value=store_record)
        repository.create_store = AsyncMock(
            return_value=ResponseStoreRecord(id=7, name="Lidl", address="Warszawa")
        )
        repository.create_receipt = AsyncMock()

        user_repository = MagicMock()
        user_repository.get_user_by_telegram_id = AsyncMock(return_value=user_record)

        client = MagicMock()
        client.messages.create = AsyncMock()

        product_service = MagicMock()
        product_service.process_product_from_receipt = AsyncMock(
            return_value=ResponseProductDomain(id=2, name="bread", unit="шт")
        )
        request_service = MagicMock()
        request_service.process_request_from_receipt = AsyncMock(
            return_value=_request_domain(22, "bread")
        )

        service = ReceiptService(
            repository, user_repository, client, product_service, request_service
        )
        return service

    return _make


@pytest.mark.asyncio
async def test_process_request_id_to_product_name(receipt_service_factory):
    service = receipt_service_factory()
    assert await service.process_request_id_to_product_name([1]) == ["milk"]


@pytest.mark.asyncio
async def test_process_update_receipt(receipt_service_factory):
    assert await receipt_service_factory().process_update_receipt() is None


@pytest.mark.asyncio
async def test_process_receipt(receipt_service_factory):
    service = receipt_service_factory()
    service.client.messages.create.return_value = _llm_response("2026-09-28T14:35:00")

    res = await service.process_receipt("img", 123, [_request_domain(11, "milk")])

    assert res is True
    service.repository.create_store.assert_awaited_once_with("Lidl", "Warszawa")
    service.product_controller.process_product_from_receipt.assert_awaited_once()
    service.request_controller.process_request_from_receipt.assert_awaited_once()

    receipt: ModelResponse = service.repository.create_receipt.await_args.args[0]
    assert receipt.receipt_date == datetime(2026, 9, 28, 14, 35)
    assert receipt.uploaded_by_user_id == 1
    assert receipt.store.id == 7
    assert [p.id for p in receipt.product] == [11, 22]


@pytest.mark.asyncio
async def test_process_receipt_existing_store(receipt_service_factory):
    service = receipt_service_factory(
        store_record=ResponseStoreRecord(id=3, name="Lidl", address="Warszawa")
    )
    service.client.messages.create.return_value = _llm_response("2026-09-28")

    assert await service.process_receipt("img", 123, [_request_domain(11, "milk")])

    service.repository.create_store.assert_not_awaited()
    receipt = service.repository.create_receipt.await_args.args[0]
    assert receipt.store.id == 3


@pytest.mark.parametrize("receipt_date", ["<UNKNOWN>", "", "2099-01-01"])
@pytest.mark.asyncio
async def test_process_receipt_unknown_date_falls_back_to_now(
    receipt_service_factory, receipt_date
):
    service = receipt_service_factory()
    service.client.messages.create.return_value = _llm_response(receipt_date)

    before = datetime.now()
    assert await service.process_receipt("img", 123, [_request_domain(11, "milk")])

    receipt = service.repository.create_receipt.await_args.args[0]
    assert receipt.receipt_date is not None
    assert before <= receipt.receipt_date <= datetime.now()


@pytest.mark.parametrize(
    "error",
    [
        APITimeoutError(request=MagicMock()),
        httpx2.TimeoutException("timeout"),
    ],
)
@pytest.mark.asyncio
async def test_process_receipt_llm_unavailable(receipt_service_factory, error):
    service = receipt_service_factory()
    service.client.messages.create.side_effect = error

    assert await service.process_receipt("img", 123, []) is False
    service.repository.create_receipt.assert_not_awaited()


@pytest.mark.asyncio
async def test_process_receipt_unknown_user(receipt_service_factory):
    service = receipt_service_factory(user_record=None)
    service.client.messages.create.return_value = _llm_response("2026-09-28")

    with pytest.raises(ValueError):
        await service.process_receipt("img", 123, [])


@pytest.mark.asyncio
async def test_process_empty_receipt(receipt_service_factory):
    service = receipt_service_factory()

    await service.process_empty_receipt(
        123, [_request_domain(11, "milk"), _request_domain(12, "bread")]
    )

    receipt: ModelResponse = service.repository.create_receipt.await_args.args[0]
    assert receipt.uploaded_by_user_id == 1
    assert receipt.store.id is None
    assert receipt.total_amount == Decimal(0)
    assert [p.id for p in receipt.product] == [11, 12]


@pytest.mark.asyncio
async def test_process_empty_receipt_unknown_user(receipt_service_factory):
    service = receipt_service_factory(user_record=None)

    with pytest.raises(ValueError):
        await service.process_empty_receipt(123, [])


@pytest.mark.asyncio
async def test_process_receipt_matches_cart_by_similar_name(receipt_service_factory):
    service = receipt_service_factory()
    service.client.messages.create.return_value = _llm_response(
        "2026-09-28", ("Молоко 2.5%", "Хлеб белый")
    )

    assert await service.process_receipt(
        "img", 123, [_request_domain(11, "молоко"), _request_domain(12, "хлеб")]
    )

    service.product_controller.process_product_from_receipt.assert_not_awaited()
    service.request_controller.process_request_from_receipt.assert_not_awaited()
    receipt = service.repository.create_receipt.await_args.args[0]
    assert [p.id for p in receipt.product] == [11, 12]


@pytest.mark.asyncio
async def test_process_receipt_matches_cart_by_product_id(receipt_service_factory):
    # receipt name is too far from the cart name, but the product found
    # by db similarity is the same product as in the cart
    service = receipt_service_factory()
    service.client.messages.create.return_value = _llm_response(
        "2026-09-28", ("Батон",)
    )

    assert await service.process_receipt(
        "img", 123, [_request_domain(11, "хлеб", product_id=2)]
    )

    service.product_controller.process_product_from_receipt.assert_awaited_once()
    service.request_controller.process_request_from_receipt.assert_not_awaited()
    receipt = service.repository.create_receipt.await_args.args[0]
    assert [p.id for p in receipt.product] == [11]


@pytest.mark.asyncio
async def test_process_receipt_closes_cart_products_missing_on_receipt(
    receipt_service_factory,
):
    service = receipt_service_factory()
    service.client.messages.create.return_value = _llm_response("2026-09-28", ("milk",))

    assert await service.process_receipt(
        "img", 123, [_request_domain(11, "milk"), _request_domain(12, "cheese")]
    )

    receipt = service.repository.create_receipt.await_args.args[0]
    assert [p.id for p in receipt.product] == [11, 12]
    missing = receipt.product[1]
    assert missing.name == "cheese"
    assert missing.price is None
    assert missing.quantity == Decimal(1)


@pytest.mark.asyncio
async def test_process_receipt_matches_cart_request_once(receipt_service_factory):
    service = receipt_service_factory()
    service.client.messages.create.return_value = _llm_response(
        "2026-09-28", ("milk", "milk")
    )

    assert await service.process_receipt("img", 123, [_request_domain(11, "milk")])

    service.request_controller.process_request_from_receipt.assert_awaited_once()
    receipt = service.repository.create_receipt.await_args.args[0]
    assert [p.id for p in receipt.product] == [11, 22]


@pytest.mark.parametrize(
    "receipt_name, cart_name, matched",
    [
        ("Молоко 2.5%", "молоко", True),
        ("Масло сливочное", "масло", True),
        ("Помидоры", "помидор", True),
        ("Сырок", "сыр", False),
        ("Чайник", "чай", False),
    ],
)
def test_match_request_by_name(
    receipt_service_factory, receipt_name, cart_name, matched
):
    service = receipt_service_factory()
    request = _request_domain(11, cart_name)

    res = service._match_request_by_name(receipt_name, [request], 85)

    assert (res is request) == matched
