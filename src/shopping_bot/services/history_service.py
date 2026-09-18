from __future__ import annotations

import logging

from shopping_bot.core.domains.history_domain import (
    LastShoppingDomain,
    StatisticsShoppingDomain,
)
from shopping_bot.core.domains.utils import (
    last_shopping_record_to_domain,
    statistics_shopping_record_to_domain,
)
from shopping_bot.core.interfaces.repository.history_repository import (
    HistoryRepositoryInterface,
)
from shopping_bot.core.interfaces.service.user_controller_interface import (
    UserControllerInterface,
)

log = logging.getLogger(__name__)


class HistoryService:
    def __init__(
        self,
        repository: HistoryRepositoryInterface,
        user_service: UserControllerInterface,
    ):
        self.repository = repository
        self.user_service = user_service

    async def process_last_shopping(self, user_telegram_id: int) -> LastShoppingDomain:
        user_id = await self.user_service.get_user_id_by_telegram_id(
            user_telegram_id=user_telegram_id
        )
        if user_id is None:
            raise ValueError()
        last_shopping_record = await self.repository.get_last_shopping(user_id)
        return last_shopping_record_to_domain(last_shopping_record)

    async def process_statistics_shopping(self) -> list[StatisticsShoppingDomain]:
        stat_shopping = await self.repository.get_statistics_shopping()
        return [
            statistics_shopping_record_to_domain(shopping) for shopping in stat_shopping
        ]
