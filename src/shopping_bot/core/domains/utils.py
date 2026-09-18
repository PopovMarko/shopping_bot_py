from shopping_bot.core.domains.history_domain import (
    LastShoppingDomain,
    LastShoppingRequestDomain,
    StatisticsRequest,
    StatisticsShoppingDomain,
)
from shopping_bot.core.domains.product_domain import (
    ProductInputResult,
    ResponseProductDomain,
    ResultProductDomain,
)
from shopping_bot.core.domains.receipt_domain import ResponseReceiptDomain
from shopping_bot.core.domains.request_domain import (
    RequestInputResult,
    ResponseRequestDomain,
    ResponseStoreDomain,
    ResultRequestDomain,
)
from shopping_bot.core.domains.user_domain import InputUserDomain, ResponseUserDomain
from shopping_bot.core.records.history_records import (
    LastShoppingRecord,
    StatisticsRequestRecord,
    StatisticsShoppingRecord,
    lastShoppingProductRecord,
)
from shopping_bot.core.records.product_records import (
    ResponseProductRecord,
)
from shopping_bot.core.records.request_records import (
    ResponseReceiptRecord,
    ResponseRequestRecord,
    ResponseStoreRecord,
)
from shopping_bot.core.records.user_records import ResponseUserRecord


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


def product_record_to_domain(product: ResponseProductRecord) -> ResponseProductDomain:
    return ResponseProductDomain(
        id=product.id,
        name=product.name,
        unit=product.unit,
        description=product.description,
    )


def user_record_to_input_domain(user: ResponseUserRecord) -> InputUserDomain:
    return InputUserDomain(
        telegram_id=user.telegram_id, name=user.name, is_admin=user.is_admin
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


def to_request_domain(
    result: RequestInputResult, request_record: ResponseRequestRecord
) -> ResultRequestDomain:
    return ResultRequestDomain(
        result=result, request_domain=to_response_request_domain(request_record)
    )


def to_response_request_domain(
    request: ResponseRequestRecord,
) -> ResponseRequestDomain:
    return ResponseRequestDomain(
        id=request.id,
        product_id=request.product_id,
        requested_by_user_id=request.requested_by_user_id,
        requested_quantity=request.requested_quantity,
        requested_at=request.requested_at,
        quantity=request.quantity,
        price=request.price,
        status=request.status,
        product=to_response_product_domain(request.product),
        requested_by_user=to_response_user_domain(request.requested_by_user),
    )


def to_response_receipt_domain(
    receipt: ResponseReceiptRecord,
) -> ResponseReceiptDomain:
    return ResponseReceiptDomain(
        id=receipt.id,
        store_id=receipt.store_id,
        uploaded_by_user_id=receipt.uploaded_by_user_id,
        receipt_date=receipt.receipt_date,
        image_url=receipt.image_url,
        raw_model_response=receipt.raw_model_response,
        created_at=receipt.created_at,
    )


def store_record_to_domain(store: ResponseStoreRecord) -> ResponseStoreDomain:
    return ResponseStoreDomain(id=store.id, name=store.name, address=store.address)


def last_shopping_product_to_domain(
    product: lastShoppingProductRecord,
) -> LastShoppingRequestDomain:
    return LastShoppingRequestDomain(
        name=product.name,
        unit=product.unit,
        quantity=product.quantity,
        price=product.price,
    )


def last_shopping_record_to_domain(shopping: LastShoppingRecord) -> LastShoppingDomain:
    list_last_shopping_products: list[LastShoppingRequestDomain] = []
    for lsh in shopping.products:
        list_last_shopping_products.append(last_shopping_product_to_domain(lsh))

    return LastShoppingDomain(
        user_name=shopping.user_name,
        last_shopping_date=shopping.shopping_date,
        store_name=shopping.store_name,
        products=list_last_shopping_products,
    )


def statistics_request_record_to_domain(
    request: StatisticsRequestRecord,
) -> StatisticsRequest:
    return StatisticsRequest(
        product_name=request.product_name,
        product_quantity=request.product_quantity,
        product_cost=request.product_cost,
    )


def statistics_shopping_record_to_domain(
    shopping: StatisticsShoppingRecord,
) -> StatisticsShoppingDomain:
    list_products_groups: list[StatisticsRequest] = []
    for r in shopping.product_groups:
        list_products_groups.append(statistics_request_record_to_domain(r))

    return StatisticsShoppingDomain(
        shoppings_ammount=shopping.shoppings_ammount,
        expences_ammount=shopping.expences_ammount,
        product_groups=list_products_groups,
    )
