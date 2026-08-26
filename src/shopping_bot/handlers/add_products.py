from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardMarkup

from shopping_bot.core.interfaces import ProductController
from shopping_bot.handlers.utils import parse_product_response
from shopping_bot.keyboards.add_product_kbd import (
    PRODUCT_CONFIRM_KBD,
)
from shopping_bot.states.user_states import WaitFor

add_router = Router()


@add_router.message(Command("добавить"))
async def add_product(message: Message, state: FSMContext) -> None:

    await state.set_state(WaitFor.product)
    await message.answer("Введите название продукта:")


@add_router.message(WaitFor.product)
async def process_add_product(
    message: Message, state: FSMContext, product_controller: ProductController
) -> None:
    if message.text is None:
        await message.answer("Enter product's name")
        return
    response = await product_controller.process_product(message.text)
    await parse_product_response(message, state, response)


@add_router.message(WaitFor.confirmation, F.text.casefold() == "yes")
async def process_confirm_product(
    message: Message, state: FSMContext, product_controller: ProductController
) -> None:
    product_id = await state.get_value("suggested_product_id")
    if product_id is None:
        raise ValueError("suggested_product_id is None")
    response = await product_controller.process_confirmation(True, product_id)
    await parse_product_response(message, state, response)


@add_router.message(WaitFor.confirmation, F.text.casefold() == "no")
async def process_not_confirm_product(
    message: Message, state: FSMContext, product_controller: ProductController
) -> None:
    response = await product_controller.process_confirmation(False, None)
    await parse_product_response(message, state, response)


@add_router.message(WaitFor.confirmation)
async def process_confirmation_invalid(message: Message) -> None:
    await message.answer(
        "Please choose Yes or No by buttons",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=PRODUCT_CONFIRM_KBD, resize_keyboard=True
        ),
    )


@add_router.message(WaitFor.quantity)
async def process_add_quantity(
    message: Message, state: FSMContext, product_controller: ProductController
) -> None:
    product_name = await state.get_value("product_name")
    product_id = await state.get_value("product_id")
    if product_id is None:
        raise ValueError("product_id it None in FSMContext")
    if message.text is None:
        await message.answer(f"Enter quantity of {product_name}")
        return
    quantity = message.text
    response = await product_controller.process_quantity(product_id, quantity)
    await parse_product_response(message, state, response)
