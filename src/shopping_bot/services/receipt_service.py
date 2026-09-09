from __future__ import annotations

import logging

from pydantic import TypeAdapter

from shopping_bot.core.domains.request_domain import (
    ResponseRequestDomain,
)
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
from shopping_bot.services.utils import (
    ModelResponse,
    Product,
    Store,
    json_response,
    llm_model_to_receipt_domain,
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
        self,
        receipt,
        user_telegram_id: int,
        request_domain_list: list[ResponseRequestDomain],
    ) -> None:
        product_name_list = [r.product.name for r in request_domain_list]

        raw_model_response = json_response
        # parse_receipt_to_json(receipt, product_name_list)
        adapter = TypeAdapter(ModelResponse)
        llm_model_response = adapter.validate_json(
            raw_model_response, strict=False, by_name=True
        )

        user_record = await self.user_repository.get_user_by_telegram_id(
            user_telegram_id
        )
        if user_record is None:
            raise ValueError("user is None in process_receipt")
        user_response_domain = to_response_user_domain(user_record)
        llm_model_response.uploaded_by_user_id = user_response_domain.id

        store_record = await self.repository.get_store_by_name_and_address(
            llm_model_response.store.name, llm_model_response.store.address
        )
        if store_record is None:
            store_record = await self.repository.create_store(
                llm_model_response.store.name, llm_model_response.store.address
            )
        store_domain = store_record_to_domain(store_record)
        llm_model_response.store.id = store_domain.id
        llm_model_response.store.name = store_domain.name
        llm_model_response.store.address = store_domain.address

        for r in request_domain_list:
            for p in llm_model_response.product:
                if r.product.name == p.name:
                    p.id = r.id

        # input_receipt_domain = llm_model_to_receipt_domain(
        #     llm_model_response, user_response_domain, raw_model_response, store_domain
        # )

        await self.repository.create_receipt(llm_model_response)
