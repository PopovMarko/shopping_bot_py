from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal


@dataclass
class lastShoppingProductRecord:
    name: str
    unit: str
    quantity: Decimal
    price: Decimal


@dataclass
class LastShoppingRecord:
    user_name: str
    shopping_date: datetime
    store_name: str
    products: list[lastShoppingProductRecord]


@dataclass
class StatisticsRequestRecord:
    product_name: str
    product_quantity: Decimal
    product_cost: Decimal


@dataclass
class StatisticsShoppingRecord:
    shoppings_ammount: int
    expences_ammount: Decimal
    product_groups: list[StatisticsRequestRecord]
