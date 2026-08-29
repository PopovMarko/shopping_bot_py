from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from shopping_bot.core.interfaces import (
    ProductControllerInterface,
)

# TODO maybe move request_router to main?
from shopping_bot.handlers.add_quantity import request_router
from shopping_bot.handlers.utils import parse_product_response
from shopping_bot.states.user_states import WaitFor

product_router = Router()
product_router.include_router(request_router)


@product_router.message(Command("добавить"))
async def add_product(message: Message, state: FSMContext) -> None:

    await state.set_state(WaitFor.product)
    await message.answer("Введите название продукта:")


@product_router.message(WaitFor.product)
async def process_add_product(
    message: Message, state: FSMContext, product_controller: ProductControllerInterface
) -> None:
    if message.text is None:
        await state.clear()
        # TODO add print list from request service
        await message.answer("Here is list of pending producs")
        return
    await state.update_data(product_name=message.text)
    response = await product_controller.process_product(message.text)
    await parse_product_response(message, state, response)


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
