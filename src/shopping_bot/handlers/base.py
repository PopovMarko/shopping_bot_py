from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

from shopping_bot.core.interfaces import UserControllerInterface
from shopping_bot.handlers.messages import (
    HELP_MESSAGE,
    ErrorMessage,
    user_domain_to_string,
)
from shopping_bot.handlers.utils import user_to_domain

router = Router()


@router.message(CommandStart())
async def start(message: Message, user_controller: UserControllerInterface):
    if message.from_user is None:
        await message.answer(ErrorMessage.INVALID_USER.value)
        return
    user = user_to_domain(message.from_user)
    response = await user_controller.start_cmd(user)
    await message.answer(user_domain_to_string(response))


@router.message(Command("help"))
async def help(message: Message):
    await message.answer(HELP_MESSAGE)
