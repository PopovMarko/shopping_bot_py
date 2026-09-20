import logging
from datetime import datetime, timedelta

from sqlalchemy import func, select
from sqlalchemy.exc import NoResultFound

from shopping_bot.core.records.history_records import (
    LastShoppingRecord,
    StatisticsRequestRecord,
    lastShoppingProductRecord,
)
from shopping_bot.db.models import (
    ProductModel,
    ReceiptModel,
    RequestModel,
    StoreModel,
    UserModel,
)
from shopping_bot.db.postgres.engine import async_session_factory
from shopping_bot.db.repository.utils import (
    last_shopping_model_to_record,
    statistics_shopping_to_record,
)

log = logging.getLogger(__name__)


class HistoryRepository:
    async def get_last_shopping(self, user_id: int) -> LastShoppingRecord:
        async with async_session_factory() as session:
            latest_receipt_id = (
                select(ReceiptModel.id)
                .where(ReceiptModel.uploaded_by_user_id == user_id)
                .order_by(ReceiptModel.receipt_date.desc().nullslast())
                .limit(1)
                .scalar_subquery()
            )

            res = await session.execute(
                select(RequestModel, ProductModel, ReceiptModel, UserModel, StoreModel)
                .join(ProductModel, ProductModel.id == RequestModel.product_id)
                .join(ReceiptModel, ReceiptModel.id == RequestModel.receipt_id)
                .join(UserModel, UserModel.id == ReceiptModel.uploaded_by_user_id)
                .outerjoin(StoreModel, StoreModel.id == ReceiptModel.store_id)
                .where(ReceiptModel.id == latest_receipt_id)
            )
            rows = res.all()
            if not rows:
                raise NoResultFound(f"No shopping history for user_id={user_id}")

            first_receipt = rows[0][2]
            first_user = rows[0][3]
            first_store = rows[0][4]

            products = [
                lastShoppingProductRecord(
                    name=product.name,
                    unit=product.unit or "",
                    quantity=request.quantity,
                    price=request.price,
                )
                for request, product, _, _, _ in rows
            ]

            return LastShoppingRecord(
                user_name=first_user.name,
                shopping_date=first_receipt.receipt_date,
                store_name=first_store.name if first_store else "",
                products=products,
            )

    async def get_statistics_shopping(self) -> list[StatisticsRequestRecord]:
        from_date = datetime.today() - timedelta(days=30)
        async with async_session_factory() as session:
            res = await session.execute(
                select(
                    ProductModel.id,
                    ProductModel.name,
                    func.sum(RequestModel.price * RequestModel.quantity).label(
                        "total_spent"
                    ),
                    func.sum(RequestModel.quantity).label(
                        "total_number",
                    ),
                )
                .join(RequestModel.product)
                .join(ReceiptModel, ReceiptModel.id == RequestModel.receipt_id)
                .where(ReceiptModel.receipt_date >= from_date)
                .group_by(ProductModel.id, ProductModel.name)
            )
            row = res.all()
            log.debug(row)
            if row is None:
                raise NoResultFound("No shopping history for")

            return [
                statistics_shopping_to_record(
                    product_name,
                    total_spent,
                    total_number,
                )
                for product_id, product_name, total_spent, total_number in row
            ]
