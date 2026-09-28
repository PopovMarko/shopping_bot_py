import base64
import io
from unittest.mock import AsyncMock, MagicMock

import pytest

from shopping_bot.handlers.add_receipt import add_receipt_photo
from shopping_bot.keyboards.main_kbd import get_main_keyboard


@pytest.fixture
def receipt_photo_message(mock_message_factory, mock_user):
    message = mock_message_factory(from_user=mock_user)
    message.photo = [MagicMock(file_id="small"), MagicMock(file_id="big")]
    return message


@pytest.fixture
def receipt_bot():
    bot = MagicMock()
    bot.get_file = AsyncMock(return_value="file")
    bot.download = AsyncMock(return_value=io.BytesIO(b"img"))
    return bot


@pytest.fixture
def mock_receipt_controller():
    controller = MagicMock()
    controller.process_receipt = AsyncMock(return_value=True)
    return controller


@pytest.mark.asyncio
async def test_add_receipt_photo(
    receipt_photo_message, mock_state, mock_receipt_controller, receipt_bot, mock_user
):
    mock_state.get_value = AsyncMock(return_value=["request"])

    await add_receipt_photo(
        receipt_photo_message, mock_state, mock_receipt_controller, receipt_bot
    )

    receipt_bot.get_file.assert_awaited_once_with("big")
    mock_receipt_controller.process_receipt.assert_awaited_once_with(
        base64.standard_b64encode(b"img").decode("utf-8"),
        mock_user.id,
        ["request"],
    )
    mock_state.clear.assert_awaited_once()
    receipt_photo_message.answer.assert_awaited_once_with(
        "Чек обработан", reply_markup=get_main_keyboard()
    )


@pytest.mark.asyncio
async def test_add_receipt_photo_not_recognized(
    receipt_photo_message, mock_state, mock_receipt_controller, receipt_bot
):
    mock_state.get_value = AsyncMock(return_value=[])
    mock_receipt_controller.process_receipt.return_value = False

    await add_receipt_photo(
        receipt_photo_message, mock_state, mock_receipt_controller, receipt_bot
    )

    mock_state.clear.assert_not_awaited()
    receipt_photo_message.answer.assert_awaited_once_with(
        "Не получилось распознать чек, попробуйте отправить фото ещё раз."
    )


@pytest.mark.asyncio
async def test_add_receipt_photo_without_user(
    receipt_photo_message, mock_state, mock_receipt_controller, receipt_bot
):
    receipt_photo_message.from_user = None
    mock_state.get_value = AsyncMock(return_value=[])

    await add_receipt_photo(
        receipt_photo_message, mock_state, mock_receipt_controller, receipt_bot
    )

    assert mock_receipt_controller.process_receipt.await_args.args[1] == 0


@pytest.mark.asyncio
async def test_add_receipt_photo_without_photo(
    receipt_photo_message, mock_state, mock_receipt_controller, receipt_bot
):
    receipt_photo_message.photo = None

    with pytest.raises(ValueError):
        await add_receipt_photo(
            receipt_photo_message, mock_state, mock_receipt_controller, receipt_bot
        )


@pytest.mark.asyncio
async def test_add_receipt_photo_download_failed(
    receipt_photo_message, mock_state, mock_receipt_controller, receipt_bot
):
    receipt_bot.download.return_value = None

    with pytest.raises(ValueError):
        await add_receipt_photo(
            receipt_photo_message, mock_state, mock_receipt_controller, receipt_bot
        )
