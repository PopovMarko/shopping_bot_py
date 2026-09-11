from typing import Protocol

from shopping_bot.core.domains.product_domain import (
    ResponseProductDomain,
    ResultProductDomain,
)


class ProductControllerInterface(Protocol):
    async def process_product(self, product_input: str) -> ResultProductDomain: ...

    async def process_confirmation(
        self, confirmed: bool, product_id: int | None, product_name: str | None
    ) -> ResultProductDomain: ...

    async def process_unit(self, unit_str: str, name: str) -> ResultProductDomain: ...

    async def process_product_from_receipt(
        self, name: str
    ) -> ResponseProductDomain: ...
