import re

from shopping_bot.core.domains.receipt_domain import (
    InputReceiptDbDomain,
    InputReceiptDomain,
)


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


def input_receipt_to_db_domain(receipt: InputReceiptDomain) -> InputReceiptDbDomain:
    if receipt.store.id is None or receipt.uploaded_by_user.id is None:
        raise ValueError("store id or user id is None in receipt creation procedure")
    return InputReceiptDbDomain(
        store_id=receipt.store.id,
        uploaded_by_user_id=receipt.uploaded_by_user.id,
        receipt_date=receipt.receipt_date,
        image_url=receipt.image_url,
        raw_model_response=receipt.raw_model_response,
        created_at=receipt.created_at,
    )
