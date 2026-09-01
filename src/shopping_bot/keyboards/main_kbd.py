from aiogram.types import InlineKeyboardMarkup, ReplyKeyboardMarkup
from aiogram.utils.keyboard import (
    InlineKeyboardBuilder,
    ReplyKeyboardBuilder,
)


def get_main_keyboard() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.button(text="/Добавить")
    builder.button(text="/Список")
    builder.button(text="/В магазине")
    builder.button(text="/На рынке")
    builder.adjust(2, 2)

    return builder.as_markup(resize_keyboard=True)


def get_cancel_keyboard() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.button(text="Хватит")
    builder.adjust(1)

    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)


def get_cancel_inline_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="Хватит", callback_data="cancel")
    builder.adjust(1)

    return builder.as_markup(resize_keyboard=True)


def get_go_to_privat_keyboard(url: str) -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.button(text="Перейти в личку", url=url)
    builder.button(text="Отмена")
    builder.adjust(1, 1)

    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)


def get_go_to_privat_inline_keyboard(url: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="Перейти в личку", url=url)
    builder.button(text="Отмена")

    return builder.as_markup(resize_keyboard=True)
