from collections.abc import Iterable
from typing import cast

from anthropic.types import MessageParam, ToolChoiceParam, ToolUnionParam


def messages_builder(
    image: str, product_name_list: list[str]
) -> Iterable[MessageParam]:
    prompt = prompt_builder(product_name_list)

    def _mesage():
        messages = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": "image/jpeg",
                            "data": image,
                        },
                    },
                    {"type": "text", "text": prompt},
                ],
            },
        ]
        return messages

    return cast(Iterable[MessageParam], _mesage())


def prompt_builder(product_name_list: list[str]):
    def f_string() -> str:
        product_list_text = "\n".join(f"- {name}" for name in product_name_list)
        prompt = f"""
        List of products currently in the cart (use them as a reference for the "name" field):
        {product_list_text}
        Parse the receipt in the photo and fill in the extract_receipt structure.
        """
        return prompt

    return f_string()


temperature = 0.0


tools: Iterable[ToolUnionParam] = [
    {
        "name": "extract_receipt",
        "description": "extract product position from receipt",
        "input_schema": {
            "type": "object",
            "properties": {
                "store": {
                    "type": "object",
                    "properties": {
                        "name": {
                            "type": "string",
                            "description": "Name of store or last name of the owner",
                        },
                        "address": {
                            "type": "string",
                            "description": "Address of the store. City and street",
                        },
                    },
                    "required": [],
                },
                "receipt_date": {"type": "string"},
                "total_amount": {"type": "string"},
                "product": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "name": {
                                "type": "string",
                                "description": """
                                                First try to map name of the product 
                                                with product_name_list in the context, if success, put the name 
                                                from product_name_list, if failed try to convert trancated name 
                                                from receipt to human readeble word and  put it instead
                                                """,
                            },
                            "price": {"type": "string"},
                            "quantity": {"type": "string"},
                            "match_confidence": {
                                "type": "string",
                                "description": """
                                                 Mark your confidence in name conversion in percent without percent mark at the end
                                                 """,
                            },
                        },
                        "required": ["name", "address"],
                    },
                },
            },
            "required": ["store", "receipt_date", "total_amount", "product"],
        },
    },
]


tool_choice: ToolChoiceParam = {
    "type": "tool",
    "name": "extract_receipt",
}

system = """
  You are an expert at recognizing product receipts from stores, written in Russian or Ukrainian or Poland languages. Your task is to extract structured data from a photo of a receipt: store information,nreceipt date, total amount, and the list of product line items.  For each product line item, first try to match the name from the receipt with one of the names from the shopping cart product list, which will be provided in the user's message. If the match is successful, use the name exactly as it appears in that list. If no name from the list is a good match, convert the abbreviated or truncated name from the receipt into a human-readable word or phrase in Russian.  For each line item, estimate your confidence in the correctness of the name match as a percentage from zero to a hundred, and put this value in the match_confidence field. If the name on the receipt is illegible or damaged, provide the most likely value and lower the confidence accordingly.  Take the store name from the receipt header; if there is no explicit chain name, use the owner's last name if it is present. Provide the address in the format of city and street, without extra details. Convert the receipt date to a unified year-month-day format.  All numeric values, such as price, quantity, and total amount, must be formatted as a string suitable for direct conversion to a number: use a period as the decimal separator, no spaces, no thousands separators, and no currency symbols. This rule applies equally to monetary amounts and to quantities, including fractional values, e.g. convert "0,5 kg" to "0.5". For example, if the receipt shows "1 234,50", output "1234.50". ",
"""
