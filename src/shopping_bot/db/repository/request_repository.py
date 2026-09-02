from dataclasses import asdict

from sqlalchemy import insert, select, update

from shopping_bot.core.domains.request_domain import (
    InputRequestDomain,
    ResponseRequestDomain,
)
from shopping_bot.core.records.request_records import ResponseRequestRecord
from shopping_bot.core.records.utils import RequestStatus
from shopping_bot.db.models import RequestModel
from shopping_bot.db.postgres.engine import async_session_factory
from shopping_bot.db.repository.utils import (
    to_request_record,
)


class RequestRepository:
    async def create_request(
        self, request: InputRequestDomain
    ) -> ResponseRequestRecord:

        async with async_session_factory() as session:
            res = await session.execute(
                insert(RequestModel).values(**asdict(request)).returning(RequestModel)
            )
            await session.commit()
            request_model = res.scalar_one()
            return to_request_record(request_model)

    async def get_request_list(
        self, *args: RequestStatus
    ) -> list[ResponseRequestRecord]:

        async with async_session_factory() as session:
            res = await session.execute(
                select(RequestModel).where(RequestModel.status.in_(args))
            )
            list_request_model = res.scalars()
            list_request_record: list[ResponseRequestRecord] = []
            for m in list_request_model:
                list_request_record.append(to_request_record(m))
            return list_request_record

    async def get_request_by_id(self, request_id: int) -> ResponseRequestRecord:
        async with async_session_factory() as session:
            res = await session.execute(
                select(RequestModel).where(RequestModel.id == request_id)
            )
            request_model = res.scalar_one()
            return to_request_record(request_model)

    async def update_request_status(
        self, request_id: int, status: RequestStatus
    ) -> None:
        async with async_session_factory() as session:
            await session.execute(
                update(RequestModel)
                .where(RequestModel.id == request_id)
                .values(status=status)
            )
            await session.commit()
