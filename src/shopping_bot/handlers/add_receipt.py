import logging
from typing import cast

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, message_auto_delete_timer_changed

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
    log.info("add_receipt_photo get photo")
    receipt = message.photo
    request_id_list: list[int] = cast(
        list[int], await state.get_value("request_id_list")
    )
    user_telegram_id = 0
    if message.from_user is not None:
        user_telegram_id = message.from_user.id
    await receipt_controller.process_receipt(receipt, user_telegram_id, request_id_list)
    await state.clear()
    await message.answer("Чек обработан", reply_markup=get_main_keyboard())
