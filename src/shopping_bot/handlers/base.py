from aiogram import Router

from aiogram.filters import CommandStart, Command
from aiogram.types import Message


router = Router()


@router.message(CommandStart())
async def start(message: Message):
    await message.answer("hello")


@router.message(Command("/new_shop"))
async def new_shop(message: Message):
    pass
