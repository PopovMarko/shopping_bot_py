from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardMarkup, User

from shopping_bot.core.domains.product_domain import (
    ProductInputResult,
    ResultProductDomain,
)
from shopping_bot.core.domains.request_domain import (
    RequestInputResult,
    ResultRequestDomain,
)
from shopping_bot.core.domains.user_domain import InputUserDomain
from shopping_bot.keyboards.add_product_kbd import (
    PRODUCT_CONFIRM_KBD,
)
from shopping_bot.states.user_states import WaitFor


def user_to_domain(user: User) -> InputUserDomain:
    id = user.id
    name = user.first_name

    return InputUserDomain(id, name)


async def parse_product_response(
    message: Message, state: FSMContext, response: ResultProductDomain
) -> None:
    match response.result:
        case ProductInputResult.PRODUCT_FOUND:
            await state.update_data(product_id=response.product_id)
            await state.update_data(product_name=response.product_name)
            await state.set_state(WaitFor.quantity)
            await message.answer(f"Enter quantity for {response.product_name}")
            return
        case ProductInputResult.PRODUCT_NOT_FOUND_NEEDS_CONFIRMATION:
            await state.update_data(suggested_product_id=response.product_id)
            await state.set_state(WaitFor.confirmation)
            await message.answer(
                f"You mean {response.product_name}?",
                reply_markup=ReplyKeyboardMarkup(
                    keyboard=PRODUCT_CONFIRM_KBD, resize_keyboard=True
                ),
            )
            return
        case ProductInputResult.PRODUCT_CREATED:
            await state.update_data(product_name=response.product_name)
            await state.set_state(WaitFor.unit)
            await message.answer(f"Choose units for {response.product_name}")
            return
        case ProductInputResult.UNIT_ACCEPTED:
            await state.set_state(WaitFor.quantity)
            await message.answer(f"Enter quantity for {response.product_name}")
            return
        case ProductInputResult.INVALID_UNIT:
            await message.answer(f"Enter valid unit for {response.product_name}")


async def parse_request_response(
    message: Message, state: FSMContext, response: ResultRequestDomain
) -> None:
    match response.result:
        case RequestInputResult.QUANTITY_ACCEPTED:
            await state.set_state(WaitFor.product)
            await message.answer("Enter next product or empty message to quit")
        case RequestInputResult.INVALID_QUANTITY:
            await message.answer("Enter correct quantity")
