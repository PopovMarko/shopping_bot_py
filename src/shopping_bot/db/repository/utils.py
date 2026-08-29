from shopping_bot.core.records.product_records import ResponseProductRecord
from shopping_bot.core.records.user_records import ResponseUserRecord
from shopping_bot.db.models import ProductModel, UserModel


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
