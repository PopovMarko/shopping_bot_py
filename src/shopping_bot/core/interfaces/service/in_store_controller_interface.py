from typing import Protocol


class InStoreControllerInterface(Protocol):
    async def process_in_store(self) -> None: ...
