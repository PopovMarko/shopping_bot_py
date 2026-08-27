from shopping_bot.core.domain import (
    RequestUserDomain,
    UserDomain,
    UserRegistrationResult,
)
from shopping_bot.core.interfaces import UserRepositoryInterface


class UserService:
    def __init__(self, repository: UserRepositoryInterface):
        self.repository = repository

    async def start_cmd(self, user: RequestUserDomain) -> UserDomain:

        find_user = await self.repository.get_user_by_telegram_id(user.telegram_id)
        status = UserRegistrationResult.REGISTERED_USER

        if find_user is None:
            find_user = await self.repository.save_user(user)
            status = UserRegistrationResult.REGISTER_USER_SUCCESS

        return UserDomain(
            msg=status,
            id=find_user.id,
            telegram_id=find_user.telegram_id,
            name=find_user.name,
        )
