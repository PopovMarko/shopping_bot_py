from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import (
    InlineKeyboardBuilder,
)

from shopping_bot.core.domains.request_domain import ResponseRequestDomain
from shopping_bot.core.records.utils import RequestStatus


def get_inline_product_list_keyboard(
    requests: list[ResponseRequestDomain],
) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for r in requests:
        checkbox = ""
        match r.status:
            case RequestStatus.in_cart | RequestStatus.fulfilled:
                checkbox = "✅"
            case RequestStatus.pending:
                checkbox = "⬜"
            case RequestStatus.cancelled:
                checkbox = "❌"
            case _:
                checkbox = "E"

        button_text = (
            f"{checkbox} {r.product.name} {r.requested_quantity} {r.product.unit}"
        )

        builder.button(text=button_text, callback_data=f"cart_{r.id}")
    builder.button(text="Закончить покупки", callback_data="stop")
    builder.adjust(1)
    return builder.as_markup()
