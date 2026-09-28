from datetime import datetime, timedelta

import pytest
from pydantic import TypeAdapter

from shopping_bot.services.utils import (
    ModelResponse,
    parse_product_input,
    parse_receipt_to_json,
)


@pytest.mark.parametrize(
    "text, expected",
    [
        ("", {"name": None, "quantity": None, "unit": None}),
        ("milk", {"name": "milk", "quantity": None, "unit": None}),
        ("milk 2", {"name": "milk", "quantity": "2", "unit": None}),
        ("milk 2 l", {"name": "milk", "quantity": "2", "unit": "l"}),
        ("milk, 2l", {"name": "milk", "quantity": "2", "unit": "l"}),
        ("red apple 0.5 кг", {"name": "red apple", "quantity": "0.5", "unit": "кг"}),
        ("2", {"name": None, "quantity": "2", "unit": None}),
    ],
)
def test_parse_product_input(text, expected):
    assert parse_product_input(text) == expected


def test_parse_receipt_to_json():
    assert parse_receipt_to_json(b"", [], "") == ""


def _receipt_date(value):
    adapter = TypeAdapter(ModelResponse)
    return adapter.validate_python(
        {
            "store": {"name": "Lidl", "address": "Warszawa"},
            "receipt_date": value,
            "total_amount": "1",
            "product": [],
        },
        strict=False,
    ).receipt_date


@pytest.mark.parametrize(
    "value, expected",
    [
        ("2026-09-28", datetime(2026, 9, 28)),
        ("2026-09-28T14:35:00", datetime(2026, 9, 28, 14, 35)),
        ("2026-09-28 14:35", datetime(2026, 9, 28, 14, 35)),
        (" 2026-09-28 ", datetime(2026, 9, 28)),
        ("28.09.2026 14:35:10", datetime(2026, 9, 28, 14, 35, 10)),
        ("28.09.2026 14:35", datetime(2026, 9, 28, 14, 35)),
        ("28.09.2026", datetime(2026, 9, 28)),
        ("28.09.26", datetime(2026, 9, 28)),
        (datetime(2026, 9, 28, 8, 0), datetime(2026, 9, 28, 8, 0)),
        ("<UNKNOWN>", None),
        ("", None),
        ("unknown", None),
        (None, None),
    ],
)
def test_receipt_date_parsing(value, expected):
    assert _receipt_date(value) == expected


def test_receipt_date_in_future_is_none():
    tomorrow = (datetime.now() + timedelta(days=1)).date().isoformat()
    assert _receipt_date(tomorrow) is None


def test_receipt_date_today_is_kept():
    today = datetime.now().date()
    assert _receipt_date(today.isoformat()) == datetime(
        today.year, today.month, today.day
    )
