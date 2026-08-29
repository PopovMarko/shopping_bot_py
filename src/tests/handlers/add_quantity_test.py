import pytest

from shopping_bot.handlers.add_quantity import process_add_quantity


@pytest.mark.parametrize(
    "text",
    ["10", None],
)
@pytest.mark.asyncio
async def test_process_add_quantity(
    mock_message_factory,
    mock_state,
    mock_product_controller,
    mock_user,
    mock_response,
    text,
):
    mock_message = mock_message_factory(from_user=mock_user, text=text)
    mock_state.get_value.side_effect = [
        mock_response.product_name,
        mock_response.product_id,
    ]

    await process_add_quantity(mock_message, mock_state, mock_product_controller)
    if mock_message.text is None:
        mock_message.answer.assert_awaited_once_with(
            f"Enter quantity of {mock_response.product_name}"
        )
    else:
        mock_product_controller.process_quantity.assert_awaited_once_with(
            mock_response.product_id, "10", 1
        )
