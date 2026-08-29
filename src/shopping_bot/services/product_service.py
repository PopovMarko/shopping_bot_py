from rapidfuzz import fuzz, process

from shopping_bot.core.domains.product_domain import (
    InputProductDomain,
    ProductInputResult,
    ResultProductDomain,
)
from shopping_bot.core.domains.utils import to_product_domain
from shopping_bot.core.interfaces import (
    ProductRepositoryInterface,
)
from shopping_bot.db.repository.utils import ResponseProductRecord


class ProductController:
    def __init__(self, repository: ProductRepositoryInterface) -> None:
        self.repository = repository

    async def process_product(
        self,
        product_name: str,
    ) -> ResultProductDomain:
        product_record_list = await self.repository.get_products()
        product_list = [i.name for i in product_record_list]
        # fuzz_result = tupl of find_name, %, index

        extraction = process.extractOne(product_name, product_list, scorer=fuzz.ratio)
        confidence = extraction[1] if extraction is not None else 0

        if confidence >= 85:
            product = product_record_list[extraction[2]]
            return to_product_domain(ProductInputResult.PRODUCT_FOUND, product)
        elif confidence >= 75:
            product = product_record_list[extraction[2]]
            return to_product_domain(
                ProductInputResult.PRODUCT_NOT_FOUND_NEEDS_CONFIRMATION, product
            )
        else:
            # product = await self.repository.create_product(product_name)
            product = ResponseProductRecord(name=product_name)
            return to_product_domain(ProductInputResult.PRODUCT_CREATED, product)

    async def process_confirmation(
        self, confirmed: bool, product_id: int | None, product_name: str
    ) -> ResultProductDomain:
        if confirmed:
            if product_id is None:
                raise ValueError(
                    "Product service get confirmed with product_id is None"
                )
            product = await self.repository.get_product(product_id)
            return to_product_domain(ProductInputResult.PRODUCT_FOUND, product)

        product = ResponseProductRecord(name=product_name)

        return to_product_domain(ProductInputResult.PRODUCT_CREATED, product)

    async def process_unit(self, unit_str: str, name: str) -> ResultProductDomain:
        if unit_str is None or name is None:
            raise ValueError
        product = InputProductDomain(name, unit_str, None)
        response = await self.repository.create_product(product)
        return to_product_domain(ProductInputResult.UNIT_ACCEPTED, response)
