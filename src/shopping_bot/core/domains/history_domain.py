from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal


@dataclass
class LastShoppingRequest:
    product_name: str
    requested_by_user: str
    requested_at: datetime


@dataclass
class LastShoppingDomain:
    store_name: str
    user_name: str
    receipt_date: datetime
    products: list[LastShoppingRequest]


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
