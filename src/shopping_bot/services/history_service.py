from __future__ import annotations

import logging

from shopping_bot.core.domains.request_domain import (
    ResponseRequestDomain,
)
from shopping_bot.core.interfaces.repository.history_repository import (
    HistoryRepositoryInterface,
)

log = logging.getLogger(__name__)


class HistoryService:
    def __init__(self, repository: HistoryRepositoryInterface):
        self.repository = repository
