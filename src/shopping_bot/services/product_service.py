import logging

from rapidfuzz import fuzz, process

from shopping_bot.core.config import Settings
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
from shopping_bot.services.utils import parse_product_input

log = logging.getLogger(__name__)


class ProductController:
    def __init__(self, repository: ProductRepositoryInterface) -> None:
        self.repository = repository

    async def process_product(
        self,
        product_input: str,
    ) -> ResultProductDomain:
        settings = Settings()
        product_record_list = await self.repository.get_products()
        product_name_list = [p.name for p in product_record_list]
        parsed_product_input: dict[str, str | None] = parse_product_input(product_input)
        log.debug(parsed_product_input)

        if parsed_product_input["name"] is None:
            raise ValueError("can't parse product_input")
        product_name = parsed_product_input["name"]

        # TODO change scorer to token scorer
        extraction = process.extractOne(
            product_name,
            product_name_list,
            scorer=fuzz.ratio,
        )
        confidence = extraction[1] if extraction is not None else 0

        if confidence >= settings.fuzzy_match_threshold:
            product: ResponseProductRecord = product_record_list[extraction[2]]
            log.debug(
                "product: %s found with confidence %d%%", product.name, confidence
            )
            return to_product_domain(ProductInputResult.PRODUCT_FOUND, product)
        elif confidence >= settings.fuzzy_confirm_threshold:
            product = product_record_list[extraction[2]]
            log.debug(
                "product: %s not found with confidence %d%%, confirmation started",
                product.name,
                confidence,
            )
            return to_product_domain(
                ProductInputResult.PRODUCT_NOT_FOUND_NEEDS_CONFIRMATION, product
            )
        else:
            product = ResponseProductRecord(name=product_name)
            log.debug(
                "product: %s not found with confidence %d%% ceration started",
                product.name,
                confidence,
            )
            product.unit = parsed_product_input["unit"]
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
