import pytest

from shopping_bot.handlers.add_products import (
    add_product,
    process_add_product,
    process_confirm_product,
)
from shopping_bot.states.user_states import WaitFor


@pytest.mark.asyncio
async def test_add_product(mock_message_factory, mock_user, mock_state):
    mock_message = mock_message_factory(from_user=mock_user, text="добавить")

    await add_product(mock_message, mock_state)

    mock_message.answer.assert_awaited_once_with("Введите название продукта:")
    mock_state.set_state.assert_awaited_once_with(WaitFor.product)


@pytest.mark.parametrize("message_text", ["milk", None])
@pytest.mark.asyncio
async def test_process_add_product(
    mock_message_factory,
    mock_user,
    mock_product_controller,
    mock_state,
    message_text,
    mock_response,
):
    mock_message = mock_message_factory(from_user=mock_user, text=message_text)

    await process_add_product(mock_message, mock_state, mock_product_controller)
    match message_text:
        case "milk":
            mock_product_controller.process_product.assert_awaited_once_with(
                mock_message.text
            )
        case None:
            mock_message.answer.assert_awaited_once_with(
                "Here is list of pending producs"
            )


@pytest.mark.parametrize(
    "text, val",
    [("yes", True), ("no", False)],
)
@pytest.mark.asyncio
async def test_process_confirm_product(
    mock_message_factory,
    mock_state,
    mock_product_controller,
    mock_response,
    mock_user,
    text,
    val,
):
    mock_message = mock_message_factory(mock_user, text)
    mock_product_controller.process_confirmation.return_value = mock_response
    mock_state.get_value.return_value = mock_response.product_id
    await process_confirm_product(mock_message, mock_state, mock_product_controller)
    if text == "yes":
        mock_state.get_value.assert_awaited_once_with("suggested_product_id")
        mock_product_controller.process_confirmation.assert_awaited_once_with(
            val, mock_response.product_id, None
        )
    # TODO issue with parameters
    else:
        mock_state.get_value.assert_awaited_once_with("product_name")
        mock_product_controller.process_confirmation.assert_awaited_once_with(
            val, None, 1
        )
