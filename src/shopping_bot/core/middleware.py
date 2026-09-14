import logging
import time

from aiogram import BaseMiddleware

log = logging.getLogger(__name__)


class TimingMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        start = time.perf_counter()
        result = await handler(event, data)
        elapsed = time.perf_counter() - start
        log.info(f"Update processed in {elapsed:.3f}s")
        return result
