from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal


@dataclass
class LastShoppingRequestDomain:
    name: str
    unit: str
    quantity: Decimal
    price: Decimal


@dataclass
class LastShoppingDomain:
    user_name: str
    last_shopping_date: datetime
    store_name: str
    products: list[LastShoppingRequestDomain]


@dataclass
class StatisticsRequest:
    product_name: str
    product_quantity: Decimal
    product_cost: Decimal


@dataclass
class StatisticsShoppingDomain:
    shoppings_ammount: int
    expences_ammount: Decimal
    product_groups: list[StatisticsRequest]
