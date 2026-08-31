from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

from shopping_bot.core.records.product_records import ResponseProductRecord
from shopping_bot.core.records.user_records import ResponseUserRecord
from shopping_bot.core.records.utils import RequestStatus


@dataclass
class ResponseRequestRecord:
    id: int
    requested_quantity: Decimal
    requested_at: datetime
    status: RequestStatus
    user: ResponseUserRecord
    product: ResponseProductRecord
