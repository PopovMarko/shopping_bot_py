from shopping_bot.core.records.product_records import ResponseProductRecord
from shopping_bot.core.records.request_records import (
    ResponseReceiptRecord,
    ResponseRequestRecord,
    ResponseStoreRecord,
)
from shopping_bot.core.records.user_records import (
    ResponseUserRecord,
)
from shopping_bot.db.models import (
    ProductModel,
    ReceiptModel,
    RequestModel,
    StoreModel,
    UserModel,
)


def user_model_to_record(user_model: UserModel) -> ResponseUserRecord:
    return ResponseUserRecord(
        id=user_model.id,
        telegram_id=user_model.telegram_id,
        name=user_model.name,
        is_admin=user_model.is_admin,
        shopping_status=user_model.shopping_status,
        active_message_id=user_model.active_message_id,
        shopping_started_at=user_model.shopping_started_at,
    )


def product_model_to_record(product: ProductModel) -> ResponseProductRecord:
    return ResponseProductRecord(
        id=product.id,
        name=product.name,
        description=product.description,
        unit=product.unit,
    )


def request_model_to_record(request: RequestModel) -> ResponseRequestRecord:
    return ResponseRequestRecord(
        id=request.id,
        product_id=request.product_id,
        requested_by_user_id=request.requested_by_user_id,
        requested_quantity=request.requested_quantity,
        requested_at=request.requested_at,
        receipt_id=request.receipt_id,
        price=request.price,
        quantity=request.quantity,
        match_confidence=request.match_confidence,
        status=request.status,
        product=product_model_to_record(request.product),
        requested_by_user=user_model_to_record(request.requested_by_user),
    )


def store_model_to_record(store: StoreModel) -> ResponseStoreRecord:
    return ResponseStoreRecord(id=store.id, name=store.name, address=store.address)


def receipt_model_to_record(receipt: ReceiptModel) -> ResponseReceiptRecord:
    return ResponseReceiptRecord(
        id=receipt.id,
        store_id=receipt.store_id,
        uploaded_by_user_id=receipt.uploaded_by_user_id,
        receipt_date=receipt.receipt_date,
        image_url=receipt.image_url,
        raw_model_response=receipt.raw_model_response,
        created_at=receipt.created_at,
    )
