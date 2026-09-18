from datetime import datetime, timedelta
from operator import and_

from sqlalchemy import func, select

from shopping_bot.core.records.history_records import (
    LastShoppingRecord,
    StatisticsShoppingRecord,
)
from shopping_bot.db.models import ProductModel, ReceiptModel, RequestModel
from shopping_bot.db.postgres.engine import async_session_factory
from shopping_bot.db.repository.utils import (
    last_shopping_model_to_record,
    statistics_shopping_to_record,
)


class HistoryRepository:
    async def get_last_shopping(self, user_id: int) -> LastShoppingRecord:
        async with async_session_factory() as session:
            res = await session.execute(
                select(RequestModel, ReceiptModel)
                .join(ReceiptModel, ReceiptModel.id == RequestModel.receipt_id)
                .where(ReceiptModel.uploaded_by_user_id == user_id)
                .order_by(ReceiptModel.receipt_date)
            )
            row = res.one()
            request_model, receipt_model = row.tuple()
            return last_shopping_model_to_record(request_model, receipt_model)


async def get_statistics_shopping(self) -> list[StatisticsShoppingRecord]:
    from_date = datetime.today() - timedelta(days=30)
    async with async_session_factory() as session:
        res = await session.execute(
            select(
                ProductModel.id,
                ProductModel.name,
                func.sum(RequestModel.price * RequestModel.quantity).label(
                    "total_spent"
                ),
            )
            .join(RequestModel.product)
            .join(ReceiptModel, ReceiptModel.id == RequestModel.receipt_id)
            .where(ReceiptModel.receipt_date >= from_date)
            .group_by(ProductModel.id, ProductModel.name)
        )
        rows = res.all()
        return [
            statistics_shopping_to_record(product_name, total_spent)
            for product_id, product_name, total_spent in rows
        ]
