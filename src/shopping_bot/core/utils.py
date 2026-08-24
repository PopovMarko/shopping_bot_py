from shopping_bot.core.repository_dto import UserRecord
from shopping_bot.db.models import UserModel


def user_model_to_record(user_model: UserModel) -> UserRecord:
    return UserRecord(
        id=user_model.id,
        telegram_id=user_model.telegram_id,
        name=user_model.name,
        is_admin=user_model.is_admin,
        shopping_status=user_model.shopping_status,
        active_message_id=user_model.active_message_id,
        shopping_started_at=user_model.shopping_started_at,
    )
