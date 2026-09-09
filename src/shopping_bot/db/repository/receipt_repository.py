from datetime import datetime
from typing import cast

from sqlalchemy import insert, select, update

from shopping_bot.core.records.request_records import (
    ResponseReceiptRecord,
    ResponseStoreRecord,
)
from shopping_bot.core.records.utils import RequestStatus
from shopping_bot.db.models import ProductModel, ReceiptModel, RequestModel, StoreModel
from shopping_bot.db.postgres.engine import async_session_factory
from shopping_bot.db.repository.utils import (
    receipt_model_to_record,
    store_model_to_record,
)
from shopping_bot.services.utils import ModelResponse


class ReceiptRepository:
    async def create_receipt(self, receipt: ModelResponse) -> ResponseReceiptRecord:
        request_id_list = []
        for r in receipt.product:
            request_id_list.append(r.id)
        async with async_session_factory() as session:
            res = await session.execute(
                insert(ReceiptModel)
                .values(
                    store_id=receipt.store.id,
                    uploaded_by_user_id=receipt.uploaded_by_user_id,
                    receipt_date=receipt.receipt_date,
                    raw_model_response=None,
                    created_at=datetime.now(),
                )
                .returning(ReceiptModel)
            )
            receipt_model = res.scalar_one()
            await session.execute(
                update(RequestModel)
                .values(receipt_id=receipt_model.id, status=RequestStatus.fulfilled)
                .where(RequestModel.id.in_(request_id_list))
            )
            await session.commit()
            return receipt_model_to_record(receipt_model)

    async def get_product_name_list(self, request_id_list: list[int]) -> list[str]:
        async with async_session_factory() as session:
            res = await session.execute(
                select(ProductModel.name)
                .join(RequestModel, ProductModel.id == RequestModel.product_id)
                .where(RequestModel.id.in_(request_id_list))
            )
            return cast(list[str], res.scalars().all())

    async def get_store_by_name_and_address(
        self,
        name: str,
        address: str | None,
    ) -> ResponseStoreRecord | None:
        async with async_session_factory() as session:
            res = await session.execute(
                select(StoreModel).where(
                    StoreModel.name == name, StoreModel.address == address
                )
            )
            store_model = res.scalar_one_or_none()
            if store_model is None:
                return None
            return store_model_to_record(store_model)

    async def create_store(self, name: str, address: str | None) -> ResponseStoreRecord:
        values: dict[str, str] = {}
        values["name"] = name
        if address is not None:
            values["address"] = address
        async with async_session_factory() as session:
            res = await session.execute(
                insert(StoreModel).values(values).returning(StoreModel)
            )
            await session.commit()
            store_model = res.scalar_one()
            return store_model_to_record(store_model)

    async def update_receipt(self) -> None: ...
