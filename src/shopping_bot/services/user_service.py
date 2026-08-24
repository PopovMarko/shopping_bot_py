from shopping_bot.core.domain import (
    RequestUserDomain,
    ResponseUserDomain,
    UserRegistrationResult,
)
from shopping_bot.core.interfaces import RepositoryController


class UserService:
    def __init__(self, repository: RepositoryController):
        self.repository = repository

    async def start_cmd(self, user: RequestUserDomain) -> ResponseUserDomain:

        find_user = await self.repository.get_user_by_telegram_id(user.telegram_id)
        status = UserRegistrationResult.REGISTERED_USER

        if find_user is None:
            find_user = await self.repository.save_user(user)
            status = UserRegistrationResult.REGISTER_USER_SUCCESS

        return ResponseUserDomain(
            msg=status,
            id=find_user.id,
            telegram_id=find_user.telegram_id,
            name=find_user.name,
        )
