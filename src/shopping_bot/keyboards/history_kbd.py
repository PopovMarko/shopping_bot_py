from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def get_history_keyboard() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.button(text="Крайний поход")
    builder.button(text="Анализ")
    builder.button(text="Вернуться")
    builder.adjust(2, 1)

    return builder.as_markup(resize_keyboard=True)
