from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel

from shopping_bot.core.domains.receipt_domain import (
    InputReceiptDomain,
)
from shopping_bot.core.domains.request_domain import ResponseStoreDomain
from shopping_bot.core.domains.user_domain import ResponseUserDomain


def parse_product_input(text: str) -> dict[str, str | None]:
    raw_parts = re.split(r"[,:\s]+", text.strip())
    parts = [p for p in raw_parts if p]

    if not parts:
        return {"name": None, "quantity": None, "unit": None}

    name_tokens: list[str] = []
    quantity: str | None = None
    unit: str | None = None

    for i, token in enumerate(parts):
        merged_match = re.match(r"^(\d+(?:[.,]\d+)?)([a-zA-Zа-яА-Я]+)$", token)
        if merged_match is not None:
            quantity, unit = merged_match.groups()
            continue

        if re.match(r"^\d+(?:[.,]\d+)?$", token):
            quantity = token
            continue

        if quantity is None:
            name_tokens.append(token)
        else:
            unit = token

    name = " ".join(name_tokens) if name_tokens else None

    return {"name": name, "quantity": quantity, "unit": unit}


def parse_receipt_to_json(receipt, product_name_list: list[str]) -> str:
    # Request LLM to parse receipt and return json
    return ""


def llm_model_to_receipt_domain(
    model_response: ModelResponse,
    user: ResponseUserDomain,
    raw_model_response: str,
    store: ResponseStoreDomain,
) -> InputReceiptDomain:
    return InputReceiptDomain(
        store_id=store.id,
        uploaded_by_user_id=user.id,
        receipt_date=model_response.receipt_date,
        image_url=None,
        raw_model_response=raw_model_response,
        created_at=datetime.now(),
    )


@dataclass
class Store(BaseModel):
    id: int | None = 1
    name: str
    address: str | None


@dataclass
class Product(BaseModel):
    id: int = 1  # ID of the Request !
    name: str
    price: Decimal
    quantity: Decimal
    match_confidence: int


@dataclass
class ModelResponse(BaseModel):
    store: Store
    uploaded_by_user_id: int | None = 1
    receipt_date: datetime
    total_ammount: Decimal
    product: list[Product]


json_response = """ 
{"store": {"name": "silpo", "address": " "}, "receipt_date": "2026-12-13", "total_ammount": "1250", "product": [{"name": "milk", "price": "33.23", "quantity": "2.5", "match_confidence": "100"}, {"name": "молоко", "price": "139", "quantity": "2.0", "match_confidence": "100"}]}

"""
# json_response = """
# {
#    "store": {
#        "name": "silpo",
#        "address": " "
#    },
#    "receipt_date": "2026-12-13",
#    "total_ammount": "1250"
#    "requests": [
#            {
#            "name": "milk"
#            "price": "33.23",
#            "quantity": "2.5",
#            "match_confidence": "100"
#        },
#            {
#            "name": "молоко"
#            "price": "139",
#            "quantity": "2.0",
#            "match_confidence": "100"
#        }
#    ]
# }
#
# """
