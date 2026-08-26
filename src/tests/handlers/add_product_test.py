import pytest

from shopping_bot.core.domain import ProductInputResult
from shopping_bot.handlers.add_products import add_product, process_add_product


@pytest.mark.asyncio
async def test_add_product(mock_message_factory, mock_user, mock_state):
    mock_message = mock_message_factory(from_user=mock_user, text="добавить")

    await add_product(mock_message, mock_state)

    mock_message.answer.assert_awaited_once_with("Введите название продукта:")
    mock_state.set_state.assert_awaited_once_with("WaitFor:product")


@pytest.mark.parametrize("message_text", [("milk",), (None,)])
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

    response = await process_add_product(
        mock_message, mock_state, mock_product_controller
    )
    match message_text:
        case "milk":
            mock_product_controller.process_product.awaited_once_with(mock_message.text)
            assert response == mock_response
        case None:
            mock_message.answer.assert_awaited_once_with("Enter product's name")


@pytest.mark.asyncio
async def test_process_confirm_product(
    mock_message_factory,
    mock_state,
    mock_product_controller,
    mock_response,
):
    mock_response.retult = ProductInputResult.PRODUCT_FOUND
    response = await mock_product_controller.process_confirmation(
        True, mock_response.suggested_product_id
    )
    assert response == mock_response
