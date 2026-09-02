import logging

from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from magic_filter.operations import call

from shopping_bot.core.interfaces.service.request_controller_interface import (
    RequestControllerInterface,
)
from shopping_bot.core.records.utils import RequestStatus
from shopping_bot.keyboards.in_store_kbd import get_inline_product_list_keyboard
from shopping_bot.keyboards.main_kbd import get_main_keyboard

log = logging.getLogger(__name__)

recipt_router = Router()

# @recipt_router(staF.photo.)
# async def add_recipt_photo(message: Message, state: FSMContext, repository: )
