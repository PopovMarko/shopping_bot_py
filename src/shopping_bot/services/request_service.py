from datetime import datetime
from decimal import Decimal, InvalidOperation

from shopping_bot.core.domains.request_domain import (
    InputRequestDomain,
    RequestInputResult,
    ResponseRequestDomain,
    ResultRequestDomain,
)
from shopping_bot.core.domains.utils import (
    to_request_domain,
    to_response_request_domain,
)
from shopping_bot.core.interfaces import (
    RequestRepositoryInterface,
    UserControllerInterface,
)
from shopping_bot.core.records.utils import RequestStatus


class RequestService:
    def __init__(
        self,
        repository: RequestRepositoryInterface,
        user_service: UserControllerInterface,
    ) -> None:
        self.repository = repository
        self.user_service = user_service

    async def process_quantity(
        self, product_id: int, quantity_str: str, telegram_user_id: int
    ) -> ResultRequestDomain:
        try:
            quantity = Decimal(quantity_str)
        except InvalidOperation:
            return ResultRequestDomain(
                RequestInputResult.INVALID_QUANTITY,
            )
        now = datetime.now()

        user_id = await self.user_service.get_user_id_by_telegram_id(telegram_user_id)
        if user_id is None:
            raise ValueError()
        request = await self.repository.create_request(
            InputRequestDomain(
                product_id=product_id,
                requested_by_user_id=user_id,
                requested_quantity=int(quantity),
                requested_at=now,
                status=RequestStatus.pending,
            )
        )
        return to_request_domain(
            RequestInputResult.QUANTITY_ACCEPTED, request, quantity
        )

    async def process_request_list(self) -> list[ResponseRequestDomain]:
        list_request_record = await self.repository.get_request_list()
        list_request_domain: list[ResponseRequestDomain] = []
        for r in list_request_record:
            list_request_domain.append(to_response_request_domain(r))
        return list_request_domain
