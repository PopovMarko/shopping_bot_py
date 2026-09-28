import importlib
from unittest.mock import AsyncMock, MagicMock, patch

import pytest


@pytest.fixture
def main_module(monkeypatch):
    # aiogram validates the token format when Bot is created
    monkeypatch.setenv("SHOPPING_BOT_TOKEN", "123456:TEST-token")
    monkeypatch.setenv("SHOPPING_BOT_CLAUDE_API_KEY", "test-key")
    with patch("shopping_bot.core.logger.logging.basicConfig"):
        module = importlib.import_module("shopping_bot.main")
    return module


def test_services_are_wired(main_module):
    assert main_module.receipt_service.repository is main_module.receipt_repository
    assert main_module.history_service.user_service is main_module.user_service
    assert main_module.webhook_url.endswith("/webhook")


@pytest.mark.asyncio
async def test_on_startup_sets_webhook(main_module):
    bot = MagicMock()
    bot.set_webhook = AsyncMock()

    await main_module.on_startup(bot)

    bot.set_webhook.assert_awaited_once_with(main_module.webhook_url)


def test_main_polling(main_module, monkeypatch):
    monkeypatch.setenv("RUN_MODE", "polling")
    with (
        patch.object(main_module.asyncio, "run") as run,
        patch.object(main_module.dp, "start_polling", MagicMock()) as start_polling,
        patch.object(main_module.web, "run_app") as run_app,
    ):
        main_module.main()

    start_polling.assert_called_once_with(main_module.bot)
    run.assert_called_once_with(start_polling.return_value)
    run_app.assert_not_called()
    assert main_module.dp.workflow_data["receipt_controller"] is (
        main_module.receipt_service
    )


def test_main_webhook(main_module, monkeypatch):
    monkeypatch.setenv("RUN_MODE", "webhook")
    with (
        patch.object(main_module, "SimpleRequestHandler") as handler,
        patch.object(main_module, "setup_application") as setup_application,
        patch.object(main_module.web, "run_app") as run_app,
        patch.object(main_module.dp.startup, "register") as register,
    ):
        main_module.main()

    register.assert_called_once_with(main_module.on_startup)
    handler.return_value.register.assert_called_once()
    setup_application.assert_called_once()
    run_app.assert_called_once()
    assert run_app.call_args.kwargs == {"host": "0.0.0.0", "port": 8080}
