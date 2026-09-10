import base64
import logging
from typing import cast

from aiogram import Bot, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

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
    message: Message,
    state: FSMContext,
    receipt_controller: ReceiptControllerInterface,
    bot: Bot,
) -> None:
    log.info("add_receipt_photo get photo ")
    if message.photo is None:
        raise ValueError()
    photo_size = message.photo[-1]
    file = await bot.get_file(photo_size.file_id)
    file_io_reader = await bot.download(file)
    if file_io_reader is None:
        raise ValueError("Failed to download file")
    img_bytes = file_io_reader.read()
    img_bytes_64 = base64.standard_b64encode(img_bytes).decode("utf-8")

    request_domain_list = cast(
        list[ResponseRequestDomain], await state.get_value("request_domain_list")
    )
    user_telegram_id = 0
    if message.from_user is not None:
        user_telegram_id = message.from_user.id

    await receipt_controller.process_receipt(
        img_bytes_64,
        user_telegram_id,
        request_domain_list,
    )
    await state.clear()
    await message.answer("Чек обработан", reply_markup=get_main_keyboard())
