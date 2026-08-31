from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, Update

from shopping_bot.core.interfaces import (
    ProductControllerInterface,
)

# TODO maybe move request_router to main?
from shopping_bot.handlers.add_quantity import request_router
from shopping_bot.handlers.utils import parse_product_response
from shopping_bot.keyboards.main_kbd import (
    get_cancel_keyboard,
    get_main_keyboard,
)
from shopping_bot.states.user_states import WaitFor

product_router = Router()
product_router.include_router(request_router)


@product_router.message(Command("Добавить"))
async def add_product(message: Message, state: FSMContext) -> None:

    await state.set_state(WaitFor.product)
    await message.answer(
        "Введите название продукта:", reply_markup=get_cancel_keyboard()
    )


@product_router.message(WaitFor.product, F.text.casefold() == "хватит")
async def cancel_product_add(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer("Список покупок составлен", reply_markup=get_main_keyboard())


@product_router.message(WaitFor.product)
async def process_add_product(
    message: Message, state: FSMContext, product_controller: ProductControllerInterface
) -> None:
    if message.text is None:
        await message.answer("Enter product name")
        return
    await state.update_data(product_name=message.text)
    response = await product_controller.process_product(message.text)
    await parse_product_response(message, state, response)


@product_router.callback_query(WaitFor.product)
async def process_cancel_add_product(
    update: Update, state: FSMContext, product_controller: ProductControllerInterface
) -> None:
    if update.callback_query is None:
        raise ValueError("Callback query is None")
    query = update.callback_query
    query.answer()
    await state.clear()


@product_router.message(WaitFor.confirmation, F.text.casefold().in_({"yes", "no"}))
async def process_confirm_product(
    message: Message, state: FSMContext, product_controller: ProductControllerInterface
) -> None:

    confirmed = False
    if message.text == "yes":
        confirmed = True

    product_id = None
    product_name = None
    if confirmed:
        product_id = await state.get_value("suggested_product_id")
        if product_id is None:
            raise ValueError("suggested_product_id is None")
    else:
        product_name = await state.get_value("product_name")
        if product_name is None:
            raise ValueError("process_add_unit - product_name is None")
    response = await product_controller.process_confirmation(
        confirmed, product_id, product_name
    )
    await parse_product_response(message, state, response)


@product_router.message(WaitFor.unit)
async def process_add_unit(
    message: Message, state: FSMContext, product_controller: ProductControllerInterface
) -> None:
    if message.text is None:
        await message.answer("Enter product's unit")
        return
    product_name = await state.get_value("product_name")
    if product_name is None:
        raise ValueError("process_add_unit - product_name is None")
    response = await product_controller.process_unit(message.text, product_name)
    await parse_product_response(message, state, response)
