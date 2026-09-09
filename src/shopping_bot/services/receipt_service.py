from __future__ import annotations

import logging

from anthropic import AsyncAnthropic
from pydantic import TypeAdapter

from shopping_bot.core.config import Settings
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
from shopping_bot.services.anthropic import (
    messages_builder,
    system,
    tool_choice,
    tools,
)
from shopping_bot.services.utils import ModelResponse

log = logging.getLogger(__name__)


class ReceiptService:
    def __init__(
        self,
        repository: ReceiptRepositoryInterface,
        user_repository: UserRepositoryInterface,
        anthropic_client: AsyncAnthropic,
    ) -> None:
        self.repository = repository
        self.user_repository = user_repository
        self.client = anthropic_client

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
        img_bytes_64: str,
        user_telegram_id: int,
        request_domain_list: list[ResponseRequestDomain],
    ) -> None:
        settings = Settings()
        product_name_list = [r.product.name for r in request_domain_list]
        messages = messages_builder(img_bytes_64, product_name_list)

        raw_model_response = await self.client.messages.create(
            model=settings.model,
            max_tokens=settings.max_tokens,
            messages=messages,
            system=system,
            tools=tools,
            tool_choice=tool_choice,
        )
        model_block = next(
            block for block in raw_model_response.content if block.type == "tool_use"
        )

        model_response_dict = model_block.input

        log.debug(f"model_response_dict {model_response_dict}")

        adapter = TypeAdapter(ModelResponse)
        llm_model_response = adapter.validate_python(
            model_response_dict, strict=False, by_name=True
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
