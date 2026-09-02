import logging

from aiogram import F, Router
from aiogram.types import CallbackQuery, Message
from magic_filter.operations import call

from shopping_bot.core.interfaces import RequestControllerInterface
from shopping_bot.core.records.utils import RequestStatus
from shopping_bot.keyboards.in_store_kbd import get_inline_product_list_keyboard
from shopping_bot.keyboards.main_kbd import get_main_keyboard

log = logging.getLogger(__name__)

store_router = Router()


@store_router.message(F.text == "/В магазине")
async def in_store(
    message: Message, request_controller: RequestControllerInterface
) -> None:
    log.info(f"in_store handler get message text {message.text}")
    request_domain_list = await request_controller.process_request_list(
        RequestStatus.in_cart, RequestStatus.pending
    )
    await message.answer(
        "Список покупок:",
        reply_markup=get_inline_product_list_keyboard(request_domain_list),
    )


@store_router.callback_query(F.data.startswith("cart_"))
async def request_in_cart_and_back(
    callback_query: CallbackQuery, request_controller: RequestControllerInterface
) -> None:
    log.info(f"request in cart and back get callback data {callback_query.data}")
    try:
        if callback_query.data is None:
            log.error("callback_query is None")
            raise ValueError()
        request_id = int(callback_query.data.split("_")[1])
    except ValueError as ex:
        log.error("invalid request_id in callback_query")
        await callback_query.answer()
        raise ValueError(ex)
    await callback_query.answer()
    request_domain_list = await request_controller.process_request_in_cart_and_back(
        request_id
    )
    if isinstance(callback_query.message, Message):
        await callback_query.message.edit_reply_markup(
            reply_markup=get_inline_product_list_keyboard(request_domain_list)
        )


@store_router.callback_query(F.data == "stop")
async def end_of_shopping(callback_query: CallbackQuery):

    log.info(f"end of shopping handler get callback data {callback_query.data}")

    if callback_query.message is not None:
        await callback_query.message.answer(
            "Покупки закончены", reply_markup=get_main_keyboard()
        )
    await callback_query.answer()
