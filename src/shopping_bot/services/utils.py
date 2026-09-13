from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel


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


def parse_receipt_to_json(
    img_bytes_64: bytes, product_name_list: list[str], prompt: str
) -> str:
    # Request LLM to parse receipt and return json
    return ""


@dataclass
class Store:
    name: str | None
    address: str | None
    id: int | None = 0


@dataclass
class Product:
    name: str
    price: Decimal | None
    quantity: Decimal | None
    match_confidence: int | None
    id: int = 0  # ID of the Request !


@dataclass
class ModelResponse:
    store: Store
    receipt_date: datetime
    total_amount: Decimal
    product: list[Product]
    uploaded_by_user_id: int | None = 0
