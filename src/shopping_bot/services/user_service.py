from shopping_bot.core.domains.user_domain import (
    InputUserDomain,
    ResultUserDomain,
    UserRegistrationResult,
)
from shopping_bot.core.interfaces import UserRepositoryInterface


class UserService:
    def __init__(self, repository: UserRepositoryInterface):
        self.repository = repository

    async def start_cmd(self, user: InputUserDomain) -> ResultUserDomain:

        find_user = await self.repository.get_user_by_telegram_id(user.telegram_id)
        status = UserRegistrationResult.REGISTERED_USER

        if find_user is None:
            find_user = await self.repository.save_user(user)
            status = UserRegistrationResult.REGISTER_USER_SUCCESS

        return ResultUserDomain(
            msg=status,
            id=find_user.id,
            telegram_id=find_user.telegram_id,
            name=find_user.name,
        )

    async def get_user_id_by_telegram_id(self, user_telegram_id: int) -> int | None:
        user = await self.repository.get_user_by_telegram_id(user_telegram_id)
        if user is None:
            return None
        return user.id
