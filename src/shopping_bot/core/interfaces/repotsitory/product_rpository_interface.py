from typing import Protocol

from shopping_bot.core.domains.product_domain import (
    InputProductDomain,
)
from shopping_bot.core.records.product_records import ResponseProductRecord


class ProductRepositoryInterface(Protocol):
    async def get_products(self) -> list[ResponseProductRecord]: ...
    async def get_product(self, id: int) -> ResponseProductRecord: ...
    async def create_product(
        self, product: InputProductDomain
    ) -> ResponseProductRecord: ...
