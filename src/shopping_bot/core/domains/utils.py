from decimal import Decimal

from shopping_bot.core.domains.product_domain import (
    ProductInputResult,
    ResponseProductDomain,
    ResultProductDomain,
)
from shopping_bot.core.domains.request_domain import (
    RequestInputResult,
    ResultRequestDomain,
)
from shopping_bot.core.domains.user_domain import ResponseUserDomain
from shopping_bot.core.records.product_records import (
    ResponseProductRecord,
)
from shopping_bot.core.records.request_records import ResponseRequestRecord
from shopping_bot.core.records.user_records import ResponseUserRecord


# TODO to think to add quantity field
def to_product_domain(
    input_result: ProductInputResult,
    product: ResponseProductRecord,
) -> ResultProductDomain:
    return ResultProductDomain(
        result=input_result,
        product_id=product.id,
        product_name=product.name,
        unit=product.unit,
    )


def to_response_product_domain(product: ResponseProductRecord) -> ResponseProductDomain:
    if product.id is None or product.unit is None or product.name is None:
        raise ValueError
    return ResponseProductDomain(
        id=product.id,
        name=product.name,
        unit=product.unit,
        description=product.description,
    )


def to_response_user_domain(user: ResponseUserRecord) -> ResponseUserDomain:
    return ResponseUserDomain(
        id=user.id,
        telegram_id=user.telegram_id,
        name=user.name,
        is_admin=user.is_admin,
        shopping_status=user.shopping_status,
        active_message_id=user.active_message_id,
        shopping_started_at=user.shopping_started_at,
    )


# TODO clear in "to_" function
def to_request_domain(
    result: RequestInputResult, request_record: ResponseRequestRecord, quantity: Decimal
) -> ResultRequestDomain:
    return ResultRequestDomain(
        result=result,
        product=to_response_product_domain(request_record.product),
        user=request_record.user,
        quantity=quantity,
        registered_at=request_record.requested_at,
        status=request_record.status,
    )
