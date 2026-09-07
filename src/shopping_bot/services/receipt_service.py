from __future__ import annotations

import logging
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel

from shopping_bot.core.domains.receipt_domain import (
    InputReceiptDomain,
)
from shopping_bot.core.domains.request_domain import ResponseStoreDomain
from shopping_bot.core.domains.user_domain import ResponseUserDomain
from shopping_bot.core.domains.utils import (
    store_record_to_domain,
    to_response_user_domain,
)
from shopping_bot.core.interfaces.repotsitory.request_repository_interface import (
    ReceiptRepositoryInterface,
)
from shopping_bot.core.interfaces.repotsitory.user_repository_interface import (
    UserRepositoryInterface,
)

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
        llm_model_response = ModelResponse.model_validate_json(raw_model_response)
        user_record = await self.user_repository.get_user_by_telegram_id(
            user_telegram_id
        )
        if user_record is None:
            raise ValueError("user is None in process_receipt")
        user_response_domain = to_response_user_domain(user_record)
        store_record = await self.repository.get_store_by_name_and_address(
            llm_model_response.store.name, llm_model_response.store.address
        )
        if store_record is None:
            store_record = await self.repository.create_store(
                llm_model_response.store.name, llm_model_response.store.address
            )
        store_domain = store_record_to_domain(store_record)
        input_receipt_domain = llm_model_to_receipt_domain(
            llm_model_response, user_response_domain, raw_model_response, store_domain
        )

        await self.repository.create_receipt(input_receipt_domain)


def llm_model_to_receipt_domain(
    model_response: ModelResponse,
    user: ResponseUserDomain,
    raw_model_response: str,
    store: ResponseStoreDomain,
) -> InputReceiptDomain:
    return InputReceiptDomain(
        store_id=store.id,
        uploaded_by_user_id=user.id,
        receipt_date=model_response.receipt_date,
        image_url=None,
        raw_model_response=raw_model_response,
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
