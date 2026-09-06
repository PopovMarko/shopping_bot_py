from __future__ import annotations

import logging
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel

from shopping_bot.core.domains.receipt_domain import (
    InputReceiptDomain,
    InputStoreDomain,
)
from shopping_bot.core.domains.user_domain import InputUserDomain, ResponseUserDomain
from shopping_bot.core.domains.utils import (
    store_record_to_domain,
    user_record_to_input_domain,
)
from shopping_bot.core.interfaces.repotsitory.request_repository_interface import (
    ReceiptRepositoryInterface,
)
from shopping_bot.core.interfaces.repotsitory.user_repository_interface import (
    UserRepositoryInterface,
)
from shopping_bot.core.records.request_records import ResponseStoreRecord
from shopping_bot.handlers.utils import (
    store_to_domain,
    user_to_domain,
)
from shopping_bot.services.utils import input_receipt_to_db_domain

log = logging.getLogger(__name__)


class ReceiptService:
    def __init__(
        self,
        repository: ReceiptRepositoryInterface,
        user_repository: UserRepositoryInterface,
    ) -> None:
        self.repository = repository
        self.user_repository = user_repository

    async def process_request_id_to_product_name(
        self,
        request_id_list: list[int],
    ) -> list[str]:
        request_list = await self.repository.get_product_name_list(request_id_list)
        return request_list

    async def process_update_receipt(self):
        pass

    async def process_receipt(
        self, receipt, user_telegram_id: int, request_id_list: list[int]
    ) -> None:
        product_name_list = await self.process_request_id_to_product_name(
            request_id_list
        )
        raw_model_response = json_response
        # parse_receipt_to_json(receipt, product_name_list)
        model_response = ModelResponse.model_validate_json(raw_model_response)
        user_record = await self.user_repository.get_user_by_telegram_id(
            user_telegram_id
        )
        if user_record is None:
            raise ValueError("user is None in process_receipt")
        user_input_domain = user_record_to_input_domain(user_record)
        input_receipt_domain = llm_model_to_receipt_domain(
            model_response, user_input_domain, raw_model_response
        )
        store_record = await self.repository.get_store_by_name_and_address(
            input_receipt_domain.store
        )
        if store_record is None:
            store_record = await self.repository.create_store(
                input_receipt_domain.store
            )
        store_domain = store_record_to_domain(store_record)
        input_db_receipt_domain = input_receipt_to_db_domain(input_receipt_domain)

        await self.repository.create_receipt(input_db_receipt_domain)


def llm_model_to_receipt_domain(
    model_response: ModelResponse, user: InputUserDomain, raw_nodel_response: str
) -> InputReceiptDomain:
    return InputReceiptDomain(
        store=store_to_domain(model_response.store),
        uploaded_by_user=user,
        receipt_date=model_response.receipt_date,
        image_url=None,
        raw_model_response=raw_nodel_response,
        created_at=datetime.now(),
    )


class Base(BaseModel):
    pass


class Store(Base):
    name: str
    address: str


class Product(Base):
    price: Decimal
    quantity: Decimal
    match_confidence: int


class ModelResponse(Base):
    store: Store
    receipt_date: datetime
    product: Product


json_response = """ 
{
   "store": {
       "name": "silpo",
       "address": " "
   },
   "receipt_date": "2026-12-13",
   "product": {
       "price": "33.23",
       "quantity": "2.5",
       "match_confidence": "100"
   }
}

"""
