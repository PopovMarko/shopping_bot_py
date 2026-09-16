import logging

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from shopping_bot.core.interfaces.service.history_controller_interface import (
    HistoryControllerInterface,
)
from shopping_bot.handlers.messages import (
    last_shopping_domain_to_string,
    statistics_shopping_to_string,
)
from shopping_bot.keyboards.history_kbd import get_history_keyboard
from shopping_bot.keyboards.main_kbd import get_main_keyboard
from shopping_bot.states.user_states import WaitFor

log = logging.getLogger(__name__)

history_router = Router()


@history_router.message(Command("История"))
async def history(message: Message, state: FSMContext) -> None:
    await state.set_state(WaitFor.history_type)
    message.answer("Нажмите кнопку", reply_markup=get_history_keyboard())


@history_router.message(WaitFor.history_type, F.text == "Вернуться")
async def return_to_main_menu(message: Message, state: FSMContext) -> None:
    await state.clear()
    message.answer("Главное меню", reply_markup=get_main_keyboard())


@history_router.message(WaitFor.history_type, F.text == "Крайний поход")
async def last_shopping(
    message: Message, state: FSMContext, history_controller: HistoryControllerInterface
) -> None:
    if message.from_user is None:
        raise ValueError()
    last_shopping = await history_controller.process_last_shopping(
        user_telegram_id=message.from_user.id
    )
    message.answer(last_shopping_domain_to_string(last_shopping))


@history_router.message(WaitFor.history_type, F.text == "Анализ")
async def statistics_shopping(
    message: Message, state: FSMContext, history_controller: HistoryControllerInterface
) -> None:
    stat_shopping = await history_controller.process_statistics_shopping()
    message.answer(statistics_shopping_to_string(stat_shopping))
