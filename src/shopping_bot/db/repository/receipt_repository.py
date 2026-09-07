from dataclasses import asdict
from typing import cast

from sqlalchemy import insert, select

from shopping_bot.core.domains.receipt_domain import (
    InputReceiptDomain,
)
from shopping_bot.core.records.request_records import (
    ResponseReceiptRecord,
    ResponseStoreRecord,
)
from shopping_bot.db.models import ProductModel, ReceiptModel, RequestModel, StoreModel
from shopping_bot.db.postgres.engine import async_session_factory
from shopping_bot.db.repository.utils import (
    receipt_model_to_record,
    store_model_to_record,
)


class ReceiptRepository:
    async def create_receipt(
        self, receipt: InputReceiptDomain
    ) -> ResponseReceiptRecord:
        async with async_session_factory() as session:
            res = await session.execute(
                insert(ReceiptModel).values(**asdict(receipt)).returning(ReceiptModel)
            )
            await session.commit()
            receipt_model = res.scalar_one()
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
        address: str,
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

    async def create_store(self, name: str, address: str) -> ResponseStoreRecord:
        async with async_session_factory() as session:
            res = await session.execute(
                insert(StoreModel).values(name, address).returning(StoreModel)
            )
            await session.commit()
            store_model = res.scalar_one()
            return store_model_to_record(store_model)

    async def update_receipt(self) -> None: ...
