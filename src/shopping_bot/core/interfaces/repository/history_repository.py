from typing import Protocol

from shopping_bot.core.records.history_records import (
    LastShoppingRecord,
    StatisticsRequestRecord,
)


class HistoryRepositoryInterface(Protocol):
    async def get_last_shopping(self, user_id: int) -> LastShoppingRecord: ...

    async def get_statistics_shopping(self) -> list[StatisticsRequestRecord]: ...
