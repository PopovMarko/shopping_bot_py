from unittest.mock import AsyncMock

import pytest

from shopping_bot.core.domains.product_domain import (
    ProductInputResult,
    ResultProductDomain,
)
from shopping_bot.handlers.add_products import (
    add_product_unit,
    cancel_product_add,
    process_add_product,
    process_confirm_product,
)
from shopping_bot.keyboards.main_kbd import get_main_keyboard
from shopping_bot.states.user_states import WaitFor

FOUND = ResultProductDomain(
    ProductInputResult.PRODUCT_FOUND, product_id=1, product_name="milk"
)


@pytest.mark.asyncio
async def test_cancel_product_add(mock_message_factory, mock_state):
    message = mock_message_factory(text="Хватит")

    await cancel_product_add(message, mock_state)

    mock_state.clear.assert_awaited_once()
    message.answer.assert_awaited_once_with(
        "Список покупок составлен", reply_markup=get_main_keyboard()
    )


@pytest.mark.asyncio
async def test_process_add_product(
    mock_message_factory, mock_state, mock_product_controller
):
    message = mock_message_factory(text="milk")
    mock_product_controller.process_product.return_value = FOUND

    await process_add_product(message, mock_state, mock_product_controller)

    mock_state.update_data.assert_any_await(product_name="milk")
    mock_product_controller.process_product.assert_awaited_once_with("milk")
    mock_state.set_state.assert_awaited_once_with(WaitFor.quantity)


@pytest.mark.asyncio
async def test_process_add_product_without_text(
    mock_message_factory, mock_state, mock_product_controller
):
    message = mock_message_factory(text=None)

    await process_add_product(message, mock_state, mock_product_controller)

    message.answer.assert_awaited_once_with("Enter product name")
    mock_product_controller.process_product.assert_not_awaited()


@pytest.mark.parametrize("text", ["yes", "no"])
@pytest.mark.asyncio
async def test_process_confirm_product_missing_state(
    mock_message_factory, mock_state, mock_product_controller, text
):
    message = mock_message_factory(text=text)
    mock_state.get_value = AsyncMock(return_value=None)

    with pytest.raises(ValueError):
        await process_confirm_product(message, mock_state, mock_product_controller)


@pytest.mark.asyncio
async def test_add_product_unit(
    mock_message_factory, mock_state, mock_product_controller
):
    message = mock_message_factory(text="l")
    mock_state.get_value = AsyncMock(return_value="milk")
    mock_product_controller.process_unit = AsyncMock(
        return_value=ResultProductDomain(
            ProductInputResult.UNIT_ACCEPTED, product_id=1, product_name="milk"
        )
    )

    await add_product_unit(message, mock_state, mock_product_controller)

    mock_product_controller.process_unit.assert_awaited_once_with("l", "milk")
    mock_state.set_state.assert_awaited_once_with(WaitFor.quantity)


@pytest.mark.asyncio
async def test_add_product_unit_without_text(
    mock_message_factory, mock_state, mock_product_controller
):
    message = mock_message_factory(text=None)

    await add_product_unit(message, mock_state, mock_product_controller)

    message.answer.assert_awaited_once_with("Enter product's unit")


@pytest.mark.asyncio
async def test_add_product_unit_without_product_name(
    mock_message_factory, mock_state, mock_product_controller
):
    message = mock_message_factory(text="l")
    mock_state.get_value = AsyncMock(return_value=None)

    with pytest.raises(ValueError):
        await add_product_unit(message, mock_state, mock_product_controller)
