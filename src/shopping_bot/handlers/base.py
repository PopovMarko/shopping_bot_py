import logging

from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from shopping_bot.core.interfaces.service.user_controller_interface import (
    UserControllerInterface,
)
from shopping_bot.handlers.messages import (
    HELP_MESSAGE,
    ErrorMessage,
    user_domain_to_string,
)
from shopping_bot.handlers.utils import user_to_domain
from shopping_bot.keyboards.main_kbd import get_main_keyboard

log = logging.getLogger(__name__)

router = Router()


@router.message(CommandStart())
async def start(message: Message, user_controller: UserControllerInterface):
    if message.from_user is None:
        await message.answer(ErrorMessage.INVALID_USER.value)
        return

    log.info(f"chat_id = {message.chat.id}, chat_type = {message.chat.type}")

    user = user_to_domain(message.from_user)
    response = await user_controller.start_cmd(user)
    await message.answer(
        user_domain_to_string(response), reply_markup=get_main_keyboard()
    )


@router.message(Command("help"))
async def help(message: Message):
    await message.answer(HELP_MESSAGE)


@router.message(F.text == "Выйти")
async def exti_shopping_bot(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer(
        "Увидимся на новом шопинге", reply_markup=ReplyKeyboardRemove()
    )
