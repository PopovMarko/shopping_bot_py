import logging
import time
from datetime import datetime
from decimal import Decimal, InvalidOperation

from shopping_bot.core.domains.product_domain import (
    ResponseProductDomain,
)
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
from shopping_bot.core.interfaces.repository.request_repository_interface import (
    RequestRepositoryInterface,
)
from shopping_bot.core.interfaces.service.user_controller_interface import (
    UserControllerInterface,
)
from shopping_bot.core.records.utils import RequestStatus

log = logging.getLogger(__name__)


class RequestService:
    def __init__(
        self,
        request_repository: RequestRepositoryInterface,
        user_service: UserControllerInterface,
    ) -> None:
        self.repository = request_repository
        self.user_service = user_service

    async def process_quantity(
        self, product_id: int, quantity_str: str, telegram_user_id: int
    ) -> ResultRequestDomain:
        try:
            quantity = Decimal(quantity_str)
        except InvalidOperation:
            return ResultRequestDomain(RequestInputResult.INVALID_QUANTITY, None)
        now = datetime.now()

        user_id = await self.user_service.get_user_id_by_telegram_id(telegram_user_id)
        if user_id is None:
            raise ValueError()
        request = await self.repository.create_request(
            InputRequestDomain(
                product_id=product_id,
                requested_by_user_id=user_id,
                requested_quantity=Decimal(quantity),
                requested_at=now,
                status=RequestStatus.pending,
                price=None,
                quantity=quantity,
            )
        )
        return to_request_domain(RequestInputResult.QUANTITY_ACCEPTED, request)

    async def process_request_list(
        self, *args: RequestStatus
    ) -> list[ResponseRequestDomain]:
        list_request_record = await self.repository.get_request_list(*args)
        list_request_domain: list[ResponseRequestDomain] = []
        for r in list_request_record:
            list_request_domain.append(to_response_request_domain(r))
        return list_request_domain

    async def process_request_in_cart_and_back(
        self, request_id: int
    ) -> list[ResponseRequestDomain]:
        t0 = time.perf_counter()
        request = await self.repository.get_request_by_id(request_id)
        log.debug(f"get_request_by_id took: {time.perf_counter() - t0:.3f}s")
        match request.status:
            case RequestStatus.pending:
                status = RequestStatus.in_cart
            case RequestStatus.in_cart:
                status = RequestStatus.pending
            case _:
                status = RequestStatus.cancelled

        t0 = time.perf_counter()
        _ = await self.repository.update_request_status(request_id, status)
        log.debug(f"update_request_status took: {time.perf_counter() - t0:.3f}s")
        t0 = time.perf_counter()
        res = await self.process_request_list(
            RequestStatus.pending, RequestStatus.in_cart
        )
        log.debug(f"process_request_list took: {time.perf_counter() - t0:.3f}s")
        return res

    async def process_request_from_receipt(
        self,
        product: ResponseProductDomain,
        requested_by_user_id: int,
        quantity: Decimal | None,
    ) -> ResponseRequestDomain:
        now = datetime.now()
        request = InputRequestDomain(
            product_id=product.id if product.id is not None else 0,
            requested_by_user_id=requested_by_user_id,
            requested_quantity=quantity if quantity is not None else Decimal(0),
            requested_at=now,
            quantity=None,
            price=None,
            status=RequestStatus.fulfilled,
        )
        request = await self.repository.create_request(request)
        return to_response_request_domain(request)
