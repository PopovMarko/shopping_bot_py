import re


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
