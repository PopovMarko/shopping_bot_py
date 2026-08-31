from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from shopping_bot.core.interfaces import RequestControllerInterface
from shopping_bot.handlers.messages import list_response_request_domain_to_string
from shopping_bot.handlers.utils import parse_request_response
from shopping_bot.states.user_states import WaitFor

request_router = Router()


@request_router.message(WaitFor.quantity)
async def process_add_quantity(
    message: Message, state: FSMContext, request_controller: RequestControllerInterface
) -> None:
    product_name = await state.get_value("product_name")
    product_id = await state.get_value("product_id")
    if product_id is None:
        raise ValueError("product_id is None in FSMContext")
    if message.text is None:
        await message.answer(f"Enter quantity of {product_name}")
        return
    quantity_str = message.text
    if message.from_user is None:
        raise ValueError
    response = await request_controller.process_quantity(
        product_id, quantity_str, message.from_user.id
    )
    await parse_request_response(message, state, response)


@request_router.message(Command("Список"))
async def list_request(
    message: Message, request_controller: RequestControllerInterface
) -> None:

    request_list = await request_controller.process_request_list()
    text_message: str = list_response_request_domain_to_string(request_list)
    await message.answer(text_message)
