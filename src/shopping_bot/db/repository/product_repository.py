from dataclasses import asdict

from sqlalchemy import insert, select

from shopping_bot.core.domains.product_domain import InputProductDomain
from shopping_bot.core.records.product_records import ResponseProductRecord
from shopping_bot.db.models import ProductModel
from shopping_bot.db.postgres.engine import async_session_factory
from shopping_bot.db.repository.utils import product_model_to_record


class ProductRepository:
    async def get_products(self) -> list[ResponseProductRecord]:

        async with async_session_factory() as session:
            res = await session.execute(select(ProductModel))
            product_models = res.scalars()
            if product_models is None:
                return []
            product_record_list: list[ResponseProductRecord] = []
            for p in product_models:
                product_record_list.append(product_model_to_record(p))
            return product_record_list

    async def get_product(self, id: int) -> ResponseProductRecord:
        if id is None:
            raise ValueError

        async with async_session_factory() as session:
            res = await session.execute(
                select(ProductModel).where(ProductModel.id == id)
            )
            product_model = res.scalar_one()
            return product_model_to_record(product_model)

    async def create_product(
        self, product: InputProductDomain
    ) -> ResponseProductRecord:
        if product is None:
            raise ValueError

        async with async_session_factory() as session:
            res = await session.execute(
                insert(ProductModel).values(**asdict(product)).returning(ProductModel)
            )
            await session.commit()
            product_model = res.scalar_one()
            return product_model_to_record(product_model)
