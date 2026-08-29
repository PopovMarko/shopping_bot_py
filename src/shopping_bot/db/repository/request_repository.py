from dataclasses import asdict

from sqlalchemy import insert

from shopping_bot.core.domains.request_domain import InputRequestDomain
from shopping_bot.core.records.request_records import ResponseRequestRecord
from shopping_bot.db.models import RequestModel
from shopping_bot.db.postgres.engine import async_session_factory
from shopping_bot.db.repository.utils import (
    product_model_to_record,
    user_model_to_record,
)


class RequestRepository:
    async def create_request(
        self, request: InputRequestDomain
    ) -> ResponseRequestRecord:

        async with async_session_factory() as session:
            res = await session.execute(
                insert(RequestModel).values(**asdict(request)).returning(RequestModel)
            )
            request_model = res.scalar_one()
            return to_request_record(request_model)


def to_request_record(request: RequestModel) -> ResponseRequestRecord:
    return ResponseRequestRecord(
        id=request.id,
        product=product_model_to_record(request.product),
        user=user_model_to_record(request.user),
        requested_quantity=request.requested_quantity,
        requested_at=request.requested_at,
        status=request.status,
    )
