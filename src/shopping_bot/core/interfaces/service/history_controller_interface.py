from typing import Protocol

from shopping_bot.core.domains.history_domain import (
    LastShoppingDomain,
    StatisticsShoppingDomain,
)


class HistoryControllerInterface(Protocol):
    async def process_last_shopping(
        self, user_telegram_id: int
    ) -> LastShoppingDomain: ...

    async def process_statistics_shopping(self) -> StatisticsShoppingDomain: ...
