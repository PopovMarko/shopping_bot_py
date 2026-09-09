import logging
from typing import cast

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, PhotoSize, message_auto_delete_timer_changed

from shopping_bot.core.domains.request_domain import ResponseRequestDomain
from shopping_bot.core.interfaces.service.request_controller_interface import (
    ReceiptControllerInterface,
)
from shopping_bot.keyboards.main_kbd import get_main_keyboard
from shopping_bot.states.user_states import WaitFor

log = logging.getLogger(__name__)

receipt_router = Router()


@receipt_router.message(WaitFor.receipt, F.photo)
async def add_receipt_photo(
    message: Message, state: FSMContext, receipt_controller: ReceiptControllerInterface
) -> None:
    log.info("add_receipt_photo get photo ")
    if message.photo is None:
        raise ValueError()
    receipt = message.photo[-1]
    request_domain_list = cast(
        list[ResponseRequestDomain], await state.get_value("request_domain_list")
    )
    user_telegram_id = 0
    if message.from_user is not None:
        user_telegram_id = message.from_user.id
    await receipt_controller.process_receipt(
        receipt, user_telegram_id, request_domain_list
    )
    await state.clear()
    await message.answer("Чек обработан", reply_markup=get_main_keyboard())
